use crate::price::Price;
use crate::{BaseLine, Exit, Filter, OHLCVSeries, Pulse, Signal, StopLoss, Strategy, OHLCV};
use std::collections::VecDeque;

const DEFAULT_LOOKBACK: usize = 55;
const DEFAULT_STOP_LEVEL: f32 = -1.0;

#[derive(Debug, PartialEq)]
pub enum TradeAction {
    GoLong(f32),
    GoShort(f32),
    ExitLong(f32),
    ExitShort(f32),
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
    filter: Box<dyn Filter>,
    pulse: Box<dyn Pulse>,
    base_line: Box<dyn BaseLine>,
    stop_loss: Box<dyn StopLoss>,
    exit: Box<dyn Exit>,
    lookback_period: usize,
}

impl BaseStrategy {
    pub fn new(
        signal: Box<dyn Signal>,
        filter: Box<dyn Filter>,
        pulse: Box<dyn Pulse>,
        base_line: Box<dyn BaseLine>,
        stop_loss: Box<dyn StopLoss>,
        exit: Box<dyn Exit>,
    ) -> Self {
        let lookbacks = [
            signal.lookback(),
            filter.lookback(),
            pulse.lookback(),
            base_line.lookback(),
            stop_loss.lookback(),
            exit.lookback(),
            DEFAULT_LOOKBACK,
        ];
        let adjusted_lookback = lookbacks.into_iter().max().unwrap_or(DEFAULT_LOOKBACK);

        Self {
            data: VecDeque::with_capacity(adjusted_lookback),
            lookback_period: adjusted_lookback,
            signal,
            filter,
            pulse,
            base_line,
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

    #[inline]
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

        let theo_price = self.suggested_entry();

        match self.trade_signals() {
            (true, _, _, _) => TradeAction::GoLong(theo_price),
            (_, true, _, _) => TradeAction::GoShort(theo_price),
            (_, _, true, _) => TradeAction::ExitLong(data.close),
            (_, _, _, true) => TradeAction::ExitShort(data.close),
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

        let (stop_loss_long, stop_loss_short) = self.stop_loss_levels();

        StopLossLevels {
            long: stop_loss_long,
            short: stop_loss_short,
        }
    }
}

impl BaseStrategy {
    fn trade_signals(&self) -> (bool, bool, bool, bool) {
        let series = self.ohlcv_series();

        let (go_long_trigger, go_short_trigger) = self.signal.generate(&series);
        let (go_long_confirm, go_short_confirm) = self.filter.confirm(&series);
        let (go_long_momentum, go_short_momentum) = self.pulse.assess(&series);
        let (go_long_filter, go_short_filter) = self.base_line.filter(&series);
        let (exit_long_eval, exit_short_eval) = self.exit.evaluate(&series);

        let prev_go_long_trigger = go_long_trigger.shift(1);
        let prev_go_short_trigger = go_short_trigger.shift(1);

        let go_long_signal = (prev_go_long_trigger | go_long_trigger)
            & go_long_confirm
            & go_long_momentum
            & go_long_filter;

        let go_short_signal = (prev_go_short_trigger | go_short_trigger)
            & go_short_confirm
            & go_short_momentum
            & go_short_filter;

        let go_long = go_long_signal.last().unwrap_or(false);
        let go_short = go_short_signal.last().unwrap_or(false);

        let exit_long = exit_long_eval.last().unwrap_or(false);
        let exit_short = exit_short_eval.last().unwrap_or(false);

        (go_long, go_short, exit_long, exit_short)
    }

    fn suggested_entry(&self) -> f32 {
        self.ohlcv_series().hlc3().last().unwrap_or(std::f32::NAN)
    }

    fn stop_loss_levels(&self) -> (f32, f32) {
        let series = self.ohlcv_series();

        let (sl_long_find, sl_short_find) = self.stop_loss.find(&series);

        let stop_loss_long = sl_long_find.last().unwrap_or(std::f32::NAN);
        let stop_loss_short = sl_short_find.last().unwrap_or(std::f32::NAN);

        (stop_loss_long, stop_loss_short)
    }
}

#[cfg(test)]
mod tests {
    use crate::price::Price;
    use crate::{
        BaseLine, BaseStrategy, Exit, Filter, OHLCVSeries, Pulse, Signal, StopLoss, Strategy,
        TradeAction, OHLCV,
    };
    use core::Series;

    struct MockSignal {
        short_period: usize,
    }

    impl Signal for MockSignal {
        fn lookback(&self) -> usize {
            self.short_period
        }

        fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.close.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    struct MockFilter {
        period: usize,
    }

    impl Filter for MockFilter {
        fn lookback(&self) -> usize {
            self.period
        }

        fn confirm(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.close.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    struct MockPulse {
        period: usize,
    }

    impl Pulse for MockPulse {
        fn lookback(&self) -> usize {
            self.period
        }

        fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.close.len();
            (Series::one(len).into(), Series::one(len).into())
        }
    }

    struct MockBaseLine {
        period: usize,
    }

    impl BaseLine for MockBaseLine {
        fn lookback(&self) -> usize {
            self.period
        }

        fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.close.len();
            (Series::one(len).into(), Series::zero(len).into())
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

        fn find(&self, data: &OHLCVSeries) -> (Series<f32>, Series<f32>) {
            let len = data.close.len();
            (
                Series::from(vec![5.0; len]) * self.multi,
                Series::from(vec![6.0; len]) * self.multi,
            )
        }
    }

    struct MockExit {}

    impl Exit for MockExit {
        fn lookback(&self) -> usize {
            0
        }

        fn evaluate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.close.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    #[test]
    fn test_base_strategy_lookback() {
        let strategy = BaseStrategy::new(
            Box::new(MockSignal { short_period: 10 }),
            Box::new(MockFilter { period: 1 }),
            Box::new(MockPulse { period: 7 }),
            Box::new(MockBaseLine { period: 15 }),
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
            Box::new(MockFilter { period: 1 }),
            Box::new(MockPulse { period: 7 }),
            Box::new(MockBaseLine { period: 15 }),
            Box::new(MockStopLoss {
                period: 2,
                multi: 2.0,
            }),
            Box::new(MockExit {}),
        );
        let lookback = 55;

        let ohlcvs = vec![
            OHLCV {
                open: 1.0,
                high: 2.0,
                low: 0.5,
                close: 1.5,
                volume: 100.0,
            };
            lookback
        ];

        let mut action = TradeAction::DoNothing;

        for ohlcv in ohlcvs {
            action = strategy.next(ohlcv);
        }

        let series = OHLCVSeries::from_data(&strategy.data);

        let hl2: Vec<f32> = series.hl2().into();
        let hlc3: Vec<f32> = series.hlc3().into();
        let hlcc4: Vec<f32> = series.hlcc4().into();
        let ohlc4: Vec<f32> = series.ohlc4().into();

        assert_eq!(hl2, vec![1.25; lookback]);
        assert_eq!(hlc3, vec![1.333_333_4; lookback]);
        assert_eq!(hlcc4, vec![1.375; lookback]);
        assert_eq!(ohlc4, vec![1.25; lookback]);
        assert_eq!(action, TradeAction::GoLong(1.333_333_4));
    }
}
