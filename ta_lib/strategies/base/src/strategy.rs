use crate::model::OHLCV;
use crate::price::Price;
use crate::OHLCVSeries;
use core::series::Series;
use std::collections::VecDeque;

const DEFAULT_LOOKBACK: usize = 55;

#[derive(Debug, PartialEq)]
pub enum TradeAction {
    GoLong(f32),
    GoShort(f32),
    ExitLong,
    ExitShort,
    DoNothing,
}

pub trait Signals {
    fn id(&self) -> String;
    fn entry(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
    fn exit(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>);
}

pub trait StopLoss {
    fn id(&self) -> String;
    fn next(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>);
}

pub trait Strategy {
    fn id(&self) -> String;
    fn next(&mut self, ohlcv: OHLCV) -> TradeAction;
    fn stop_loss(&self) -> (f32, f32);
}

pub struct BaseStrategy<S: Signals, L: StopLoss> {
    data: VecDeque<OHLCV>,
    signal: S,
    stop_loss: L,
    lookback_period: usize,
}

impl<S: Signals, L: StopLoss> BaseStrategy<S, L> {
    pub fn new(signal: S, stop_loss: L, lookback_period: usize) -> Self {
        let adjusted_lookback = std::cmp::max(lookback_period, DEFAULT_LOOKBACK);

        Self {
            data: VecDeque::with_capacity(adjusted_lookback),
            lookback_period: adjusted_lookback,
            signal,
            stop_loss,
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
}

impl<S: Signals, L: StopLoss> Strategy for BaseStrategy<S, L> {
    fn id(&self) -> String {
        format!("_STRTG{}_STPLSS{}", self.signal.id(), self.stop_loss.id())
    }

    fn next(&mut self, data: OHLCV) -> TradeAction {
        self.store(data);

        if !self.can_process() {
            return TradeAction::DoNothing;
        }

        let series = OHLCVSeries::from_data(&self.data);

        let (go_long_series, go_short_series) = self.signal.entry(&series);
        let (exit_long_series, exit_short_series) = self.signal.exit(&series);

        let go_long = go_long_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();
        let go_short = go_short_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();
        let exit_long = exit_long_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();
        let exit_short = exit_short_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();

        let suggested_entry = series.hlc3().last().unwrap_or(&std::f32::NAN).clone();

        match (go_long, go_short, exit_long, exit_short) {
            (true, _, _, _) => TradeAction::GoLong(suggested_entry),
            (_, true, _, _) => TradeAction::GoShort(suggested_entry),
            (_, _, true, _) => TradeAction::ExitLong,
            (_, _, _, true) => TradeAction::ExitShort,
            _ => TradeAction::DoNothing,
        }
    }

    fn stop_loss(&self) -> (f32, f32) {
        if !self.can_process() {
            return (-1.0, -1.0);
        }

        let series = OHLCVSeries::from_data(&self.data);

        let (stop_loss_long_series, stop_loss_short_series) = self.stop_loss.next(&series);

        let stop_loss_long = stop_loss_long_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();

        let stop_loss_short = stop_loss_short_series
            .into_iter()
            .flatten()
            .last()
            .unwrap_or_default();

        (stop_loss_long, stop_loss_short)
    }
}

#[cfg(test)]
mod tests {
    use crate::price::Price;
    use crate::strategy::{StopLoss, Strategy};
    use crate::{BaseStrategy, OHLCVSeries, Signals, OHLCV};
    use core::series::Series;

    struct MockStrategy {
        short_period: usize,
    }

    impl Signals for MockStrategy {
        fn id(&self) -> String {
            format!("MOCK_{}", self.short_period)
        }

        fn entry(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (Series::empty(1), Series::empty(1))
        }

        fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (Series::empty(1), Series::empty(1))
        }
    }

    struct MockStopLoss {
        multi: f32,
    }

    impl StopLoss for MockStopLoss {
        fn id(&self) -> String {
            format!("SL_{:.1}", self.multi)
        }

        fn next(&self, _data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
            (
                Series::from([5.0]) * self.multi,
                Series::from([6.0]) * self.multi,
            )
        }
    }

    #[test]
    fn test_base_strategy_lookback() {
        let strategy = BaseStrategy::new(
            MockStrategy { short_period: 10 },
            MockStopLoss { multi: 2.0 },
            2,
        );
        assert_eq!(strategy.lookback_period, 55);
    }

    #[test]
    fn test_base_strategy_id() {
        let strategy = BaseStrategy::new(
            MockStrategy { short_period: 10 },
            MockStopLoss { multi: 2.0 },
            2,
        );
        assert_eq!(strategy.id(), "_STRTGMOCK_10_STPLSSSL_2.0");
    }

    #[test]
    fn test_strategy_data() {
        let mut strategy = BaseStrategy::new(
            MockStrategy { short_period: 10 },
            MockStopLoss { multi: 2.0 },
            3,
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

        assert_eq!(series.open, vec![1.0, 2.0, 3.0, 4.0]);
        assert_eq!(series.high, vec![2.0, 3.0, 4.0, 5.0]);
        assert_eq!(series.low, vec![0.5, 1.5, 2.5, 3.5]);
        assert_eq!(series.close, vec![1.5, 2.5, 3.5, 4.5]);
        assert_eq!(series.volume, vec![100.0, 200.0, 300.0, 400.0]);

        assert_eq!(series.hl2(), vec![1.25, 2.25, 3.25, 4.25]);
        assert_eq!(
            series.hlc3(),
            vec![
                1.3333333333333333,
                2.3333333333333335,
                3.3333333333333335,
                4.333333333333333
            ]
        );
        assert_eq!(series.hlcc4(), vec![1.375, 2.375, 3.375, 4.375]);
        assert_eq!(series.ohlc4(), vec![1.25, 2.25, 3.25, 4.25]);
    }
}
