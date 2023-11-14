use crate::price::Price;
use crate::{Exit, OHLCVSeries, Regime, Signal, StopLoss, Strategy, Volume, OHLCV};
use std::collections::VecDeque;

const DEFAULT_LOOKBACK: usize = 55;
const DEFAULT_STOP_LEVEL: f32 = -1.0;

#[derive(Debug, PartialEq)]
pub enum TradeAction {
    GoLong(f32),
    GoShort(f32),
    ExitLong,
    ExitShort,
    DoNothing,
}

#[derive(Debug)]
pub struct StopLossLevels {
    pub long: f32,
    pub short: f32,
}

pub struct BaseStrategy {
    data: VecDeque<OHLCV>,
    signal: Box<dyn Signal>,
    regime: Box<dyn Regime>,
    volume: Box<dyn Volume>,
    stop_loss: Box<dyn StopLoss>,
    exit: Box<dyn Exit>,
    lookback_period: usize,
}

impl BaseStrategy {
    pub fn new(
        signal: Box<dyn Signal>,
        regime: Box<dyn Regime>,
        volume: Box<dyn Volume>,
        stop_loss: Box<dyn StopLoss>,
        exit: Box<dyn Exit>,
    ) -> Self {
        let lookbacks = [
            signal.lookback(),
            regime.lookback(),
            volume.lookback(),
            stop_loss.lookback(),
            exit.lookback(),
            DEFAULT_LOOKBACK,
        ];
        let adjusted_lookback = lookbacks.iter().cloned().max().unwrap_or(DEFAULT_LOOKBACK);

        Self {
            data: VecDeque::with_capacity(adjusted_lookback),
            lookback_period: adjusted_lookback,
            signal,
            regime,
            volume,
            stop_loss,
            exit,
        }
    }

    fn store(&mut self, data: OHLCV) {
        if self.data.len() >= self.lookback_period {
            self.data.pop_front();
        }

        self.data.push_back(data);
    }

    fn can_process(&self) -> bool {
        self.data.len() >= self.lookback_period
    }

    fn ohlcv_series(&self) -> OHLCVSeries {
        OHLCVSeries::from_data(&self.data)
    }
}

impl Strategy for BaseStrategy {
    fn next(&mut self, data: OHLCV) -> TradeAction {
        self.store(data);

        if !self.can_process() {
            return TradeAction::DoNothing;
        }

        let series = self.ohlcv_series();

        match self.trade_signals(&series) {
            (true, _, _, _) => TradeAction::GoLong(self.suggested_entry(&series)),
            (_, true, _, _) => TradeAction::GoShort(self.suggested_entry(&series)),
            (_, _, true, _) => TradeAction::ExitLong,
            (_, _, _, true) => TradeAction::ExitShort,
            _ => TradeAction::DoNothing,
        }
    }

    fn stop_loss(&self) -> StopLossLevels {
        if !self.can_process() {
            return StopLossLevels {
                long: DEFAULT_STOP_LEVEL,
                short: DEFAULT_STOP_LEVEL,
            };
        }

        let series = self.ohlcv_series();
        let (stop_loss_long, stop_loss_short) = self.stop_loss_levels(&series);

        StopLossLevels {
            long: stop_loss_long,
            short: stop_loss_short,
        }
    }
}

impl BaseStrategy {
    fn trade_signals(&self, series: &OHLCVSeries) -> (bool, bool, bool, bool) {
        let (go_long_signal, go_short_signal) = self.signal.generate(series);
        let (go_long_regime, go_short_regime) = self.regime.apply(series);
        let (go_long_volume, go_short_volume) = self.volume.apply(series);

        let go_long_series = go_long_signal & go_long_regime & go_long_volume;
        let go_short_series = go_short_signal & go_short_regime & go_short_volume;

        let (exit_long_series, exit_short_series) = self.exit.generate(series);

        let go_long = go_long_series.last().unwrap_or_default();
        let go_short = go_short_series.last().unwrap_or_default();
        let exit_long = exit_long_series.last().unwrap_or_default();
        let exit_short = exit_short_series.last().unwrap_or_default();

        (go_long, go_short, exit_long, exit_short)
    }

    fn suggested_entry(&self, series: &OHLCVSeries) -> f32 {
        series.hlc3().last().unwrap_or(std::f32::NAN)
    }

    fn stop_loss_levels(&self, series: &OHLCVSeries) -> (f32, f32) {
        let (stop_loss_long_series, stop_loss_short_series) = self.stop_loss.next(series);

        let stop_loss_long = stop_loss_long_series.last().unwrap_or_default();
        let stop_loss_short = stop_loss_short_series.last().unwrap_or_default();

        (stop_loss_long, stop_loss_short)
    }
}

#[cfg(test)]
mod tests {
    use crate::price::Price;
    use crate::{
        BaseStrategy, Exit, OHLCVSeries, Regime, Signal, StopLoss, Strategy, Volume, OHLCV,
    };
    use core::Series;

    struct MockSignal {
        short_period: usize,
    }

    impl Signal for MockSignal {
        fn lookback(&self) -> usize {
            self.short_period
        }

        fn generate(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (Series::empty(1), Series::empty(1))
        }
    }

    struct MockExit {}

    impl Exit for MockExit {
        fn lookback(&self) -> usize {
            0
        }

        fn generate(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (Series::empty(1), Series::empty(1))
        }
    }

    struct MockStopLoss {
        period: usize,
        multi: f32,
    }

    impl StopLoss for MockStopLoss {
        fn lookback(&self) -> usize {
            self.period
        }

        fn next(&self, _data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
            (
                Series::from([5.0]) * self.multi,
                Series::from([6.0]) * self.multi,
            )
        }
    }

    struct MockRegime {
        period: usize,
    }

    impl Regime for MockRegime {
        fn lookback(&self) -> usize {
            self.period
        }

        fn apply(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (
                Series::empty(1).nz(Some(0.0)).into(),
                Series::empty(1).nz(Some(0.0)).into(),
            )
        }
    }

    struct MockVolume {
        period: usize,
    }

    impl Volume for MockVolume {
        fn lookback(&self) -> usize {
            self.period
        }

        fn apply(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (
                Series::empty(1).nz(Some(0.0)).into(),
                Series::empty(1).nz(Some(0.0)).into(),
            )
        }
    }

    #[test]
    fn test_base_strategy_lookback() {
        let strategy = BaseStrategy::new(
            Box::new(MockSignal { short_period: 10 }),
            Box::new(MockRegime { period: 1 }),
            Box::new(MockVolume { period: 15 }),
            Box::new(MockStopLoss {
                period: 2,
                multi: 2.0,
            }),
            Box::new(MockExit {}),
        );
        assert_eq!(strategy.lookback_period, 55);
    }

    #[test]
    fn test_strategy_data() {
        let mut strategy = BaseStrategy::new(
            Box::new(MockSignal { short_period: 10 }),
            Box::new(MockRegime { period: 1 }),
            Box::new(MockVolume { period: 15 }),
            Box::new(MockStopLoss {
                period: 2,
                multi: 2.0,
            }),
            Box::new(MockExit {}),
        );
        let ohlcvs = vec![
            OHLCV {
                open: 1.0,
                high: 2.0,
                low: 0.5,
                close: 1.5,
                volume: 100.0,
            },
            OHLCV {
                open: 2.0,
                high: 3.0,
                low: 1.5,
                close: 2.5,
                volume: 200.0,
            },
            OHLCV {
                open: 3.0,
                high: 4.0,
                low: 2.5,
                close: 3.5,
                volume: 300.0,
            },
            OHLCV {
                open: 4.0,
                high: 5.0,
                low: 3.5,
                close: 4.5,
                volume: 400.0,
            },
        ];

        for ohlcv in ohlcvs {
            strategy.next(ohlcv);
        }

        let series = OHLCVSeries::from_data(&strategy.data);
        let open: Vec<f32> = series.open.clone().into();
        let high: Vec<f32> = series.high.clone().into();
        let low: Vec<f32> = series.low.clone().into();
        let close: Vec<f32> = series.close.clone().into();
        let volume: Vec<f32> = series.volume.clone().into();

        let hl2: Vec<f32> = series.hl2().into();
        let hlc3: Vec<f32> = series.hlc3().into();
        let hlcc4: Vec<f32> = series.hlcc4().into();
        let ohlc4: Vec<f32> = series.ohlc4().into();

        assert_eq!(open, vec![1.0, 2.0, 3.0, 4.0]);
        assert_eq!(high, vec![2.0, 3.0, 4.0, 5.0]);
        assert_eq!(low, vec![0.5, 1.5, 2.5, 3.5]);
        assert_eq!(close, vec![1.5, 2.5, 3.5, 4.5]);
        assert_eq!(volume, vec![100.0, 200.0, 300.0, 400.0]);

        assert_eq!(hl2, vec![1.25, 2.25, 3.25, 4.25]);
        assert_eq!(
            hlc3,
            vec![1.333_333_4, 2.333_333_3, 3.333_333_3, 4.333_333_5]
        );
        assert_eq!(hlcc4, vec![1.375, 2.375, 3.375, 4.375]);
        assert_eq!(ohlc4, vec![1.25, 2.25, 3.25, 4.25]);
    }
}
