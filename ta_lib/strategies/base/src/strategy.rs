use crate::source::{Source, SourceType};
use crate::{BaseLine, Confirm, Exit, OHLCVSeries, Pulse, Signal, StopLoss, Strategy, OHLCV};
use std::collections::VecDeque;

const DEFAULT_LOOKBACK: usize = 55;
const DEFAULT_STOP_LEVEL: f32 = -1.0;
const DEFAULT_BUFF_SIZE: f32 = 1.236;

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
    confirm: Box<dyn Confirm>,
    pulse: Box<dyn Pulse>,
    base_line: Box<dyn BaseLine>,
    stop_loss: Box<dyn StopLoss>,
    exit: Box<dyn Exit>,
    lookback_period: usize,
}

impl BaseStrategy {
    pub fn new(
        signal: Box<dyn Signal>,
        confirm: Box<dyn Confirm>,
        pulse: Box<dyn Pulse>,
        base_line: Box<dyn BaseLine>,
        stop_loss: Box<dyn StopLoss>,
        exit: Box<dyn Exit>,
    ) -> Self {
        let lookbacks = [
            signal.lookback(),
            confirm.lookback(),
            pulse.lookback(),
            base_line.lookback(),
            stop_loss.lookback(),
            exit.lookback(),
            DEFAULT_LOOKBACK,
        ];
        let lookback_period = lookbacks.into_iter().max().unwrap_or(DEFAULT_LOOKBACK);

        Self {
            data: VecDeque::with_capacity(lookback_period),
            signal,
            confirm,
            pulse,
            base_line,
            stop_loss,
            exit,
            lookback_period,
        }
    }

    fn store(&mut self, data: OHLCV) {
        let buf_size = (self.lookback_period as f32 * DEFAULT_BUFF_SIZE) as usize;

        if self.data.len() > buf_size {
            self.data.pop_front();
        }

        self.data.push_back(data);
    }

    #[inline(always)]
    fn can_process(&self) -> bool {
        self.data.len() >= self.lookback_period
    }

    #[inline(always)]
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
            (true, false, false, false) => TradeAction::GoLong(theo_price),
            (false, true, false, false) => TradeAction::GoShort(theo_price),
            (false, false, true, false) => TradeAction::ExitLong(theo_price),
            (false, false, false, true) => TradeAction::ExitShort(theo_price),
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
        let (go_long_baseline, go_short_baseline) = self.base_line.generate(&series);
        let (go_long_confirm, go_short_confirm) = self.confirm.validate(&series);
        let (go_long_momentum, go_short_momentum) = self.pulse.assess(&series);
        let (filter_long_baseline, filter_short_baseline) = self.base_line.filter(&series);
        let (exit_long_eval, exit_short_eval) = self.exit.evaluate(&series);

        let go_long_signal = go_long_trigger | go_long_baseline;
        let go_short_signal = go_short_trigger | go_short_baseline;

        let go_long = (go_long_signal & filter_long_baseline & go_long_confirm & go_long_momentum)
            .last()
            .unwrap_or(false);
        let go_short =
            (go_short_signal & filter_short_baseline & go_short_confirm & go_short_momentum)
                .last()
                .unwrap_or(false);

        let exit_long = exit_long_eval.last().unwrap_or(false);
        let exit_short = exit_short_eval.last().unwrap_or(false);

        (go_long, go_short, exit_long, exit_short)
    }

    fn suggested_entry(&self) -> f32 {
        self.ohlcv_series()
            .source(SourceType::OHLC4)
            .last()
            .unwrap_or(std::f32::NAN)
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
    use crate::source::{Source, SourceType};
    use crate::{
        BaseLine, BaseStrategy, Confirm, Exit, OHLCVSeries, Pulse, Signal, StopLoss, Strategy,
        TradeAction, OHLCV,
    };
    use core::Series;

    const DEFAULT_BUFF_SIZE: f32 = 1.3;
    const DEFAULT_LOOKBACK: usize = 55;

    struct MockSignal {
        fast_period: usize,
    }

    impl Signal for MockSignal {
        fn lookback(&self) -> usize {
            self.fast_period
        }

        fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    struct MockConfirm {
        period: usize,
    }

    impl Confirm for MockConfirm {
        fn lookback(&self) -> usize {
            self.period
        }

        fn validate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
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
            let len = data.len();
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

        fn generate(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
            (Series::one(len).into(), Series::zero(len).into())
        }

        fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
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
            let len = data.len();
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
            let len = data.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    #[test]
    fn test_base_strategy_lookback() {
        let strategy = BaseStrategy::new(
            Box::new(MockSignal { fast_period: 10 }),
            Box::new(MockConfirm { period: 1 }),
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
            Box::new(MockSignal { fast_period: 10 }),
            Box::new(MockConfirm { period: 1 }),
            Box::new(MockPulse { period: 7 }),
            Box::new(MockBaseLine { period: 15 }),
            Box::new(MockStopLoss {
                period: 2,
                multi: 2.0,
            }),
            Box::new(MockExit {}),
        );
        let lookback = (DEFAULT_BUFF_SIZE * DEFAULT_LOOKBACK as f32) as usize;
        let data = OHLCV {
            ts: 1710297600000,
            open: 1.0,
            high: 2.0,
            low: 0.5,
            close: 1.5,
            volume: 100.0,
        };
        let ohlcvs = vec![data; lookback];

        let mut action = TradeAction::DoNothing;

        for ohlcv in ohlcvs {
            action = strategy.next(ohlcv);
        }

        let series = OHLCVSeries::from_data(&strategy.data);

        let hl2: Vec<f32> = series.source(SourceType::HL2).into();
        let hlc3: Vec<f32> = series.source(SourceType::HLC3).into();
        let hlcc4: Vec<f32> = series.source(SourceType::HLCC4).into();
        let ohlc4: Vec<f32> = series.source(SourceType::OHLC4).into();

        assert_eq!(hl2, vec![1.25]);
        assert_eq!(hlc3, vec![1.333_333_4]);
        assert_eq!(hlcc4, vec![1.375]);
        assert_eq!(ohlc4, vec![1.25]);
        assert_eq!(action, TradeAction::DoNothing);
    }
}
