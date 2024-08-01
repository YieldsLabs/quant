use crate::source::{Source, SourceType};
use crate::{BaseLine, Confirm, Exit, Pulse, Signal, StopLoss, Strategy};
use timeseries::prelude::*;

const DEFAULT_LOOKBACK: usize = 210;
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
    timeseries: Box<dyn TimeSeries>,
    signal: Box<dyn Signal>,
    primary_confirm: Box<dyn Confirm>,
    secondary_confirm: Box<dyn Confirm>,
    pulse: Box<dyn Pulse>,
    base_line: Box<dyn BaseLine>,
    stop_loss: Box<dyn StopLoss>,
    exit: Box<dyn Exit>,
    lookback_period: usize,
}

impl BaseStrategy {
    pub fn new(
        timeseries: Box<dyn TimeSeries>,
        signal: Box<dyn Signal>,
        primary_confirm: Box<dyn Confirm>,
        secondary_confirm: Box<dyn Confirm>,
        pulse: Box<dyn Pulse>,
        base_line: Box<dyn BaseLine>,
        stop_loss: Box<dyn StopLoss>,
        exit: Box<dyn Exit>,
    ) -> Self {
        let lookbacks = [
            signal.lookback(),
            primary_confirm.lookback(),
            secondary_confirm.lookback(),
            pulse.lookback(),
            base_line.lookback(),
            stop_loss.lookback(),
            exit.lookback(),
            DEFAULT_LOOKBACK,
        ];
        let lookback_period = lookbacks.into_iter().max().unwrap_or(DEFAULT_LOOKBACK);

        Self {
            timeseries,
            signal,
            primary_confirm,
            secondary_confirm,
            pulse,
            base_line,
            stop_loss,
            exit,
            lookback_period,
        }
    }

    fn store(&mut self, bar: &OHLCV) {
        self.timeseries.add(bar)
    }

    #[inline(always)]
    fn can_process(&self) -> bool {
        self.timeseries.len() >= self.lookback_period
    }

    fn ohlcv(&self) -> OHLCVSeries {
        self.timeseries.ohlcv(self.lookback_period)
    }
}

impl Strategy for BaseStrategy {
    fn next(&mut self, bar: &OHLCV) -> TradeAction {
        self.store(bar);

        if !self.can_process() {
            return TradeAction::DoNothing;
        }

        let ohlcv = self.ohlcv();
        let bar_index = ohlcv.bar_index(bar);
        let theo_price = self.suggested_entry(&ohlcv);

        match self.trade_signals(&ohlcv, bar_index) {
            (true, _, _, _) => TradeAction::GoLong(theo_price),
            (_, true, _, _) => TradeAction::GoShort(theo_price),
            (_, _, true, _) => TradeAction::ExitLong(theo_price),
            (_, _, _, true) => TradeAction::ExitShort(theo_price),
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

        let ohlcv = self.ohlcv();
        let (stop_loss_long, stop_loss_short) = self.stop_loss_levels(&ohlcv);

        StopLossLevels {
            long: stop_loss_long,
            short: stop_loss_short,
        }
    }
}

impl BaseStrategy {
    fn trade_signals(&self, ohlcv: &OHLCVSeries, bar_index: usize) -> (bool, bool, bool, bool) {
        let (signal_go_long, signal_go_short) = self.signal.trigger(ohlcv);

        let (baseline_confirm_long, baseline_confirm_short) = self.base_line.filter(ohlcv);
        let (primary_confirm_long, primary_confirm_short) = self.primary_confirm.filter(ohlcv);
        let (pulse_confirm_long, pulse_confirm_short) = self.pulse.assess(ohlcv);

        let (exit_close_long, exit_close_short) = self.exit.close(ohlcv);
        let (baseline_close_long, baseline_close_short) = self.base_line.close(ohlcv);

        let confirm_long = pulse_confirm_long & primary_confirm_long;
        let confirm_short = pulse_confirm_short & primary_confirm_short;

        let base_go_long = signal_go_long & baseline_confirm_long & confirm_long;
        let base_go_short = signal_go_short & baseline_confirm_short & confirm_short;

        let go_long = base_go_long.get(bar_index).unwrap_or(false);
        let go_short = base_go_short.get(bar_index).unwrap_or(false);

        let exit_long = (exit_close_long | baseline_close_long)
            .get(bar_index)
            .unwrap_or(false);
        let exit_short = (exit_close_short | baseline_close_short)
            .get(bar_index)
            .unwrap_or(false);

        (go_long, go_short, exit_long, exit_short)
    }

    fn suggested_entry(&self, ohlcv: &OHLCVSeries) -> f32 {
        ohlcv.source(SourceType::CLOSE).last().unwrap_or(f32::NAN)
    }

    fn stop_loss_levels(&self, ohlcv: &OHLCVSeries) -> (f32, f32) {
        let (sl_long_find, sl_short_find) = self.stop_loss.find(ohlcv);

        let stop_loss_long = sl_long_find.last().unwrap_or(f32::NAN);
        let stop_loss_short = sl_short_find.last().unwrap_or(f32::NAN);

        (stop_loss_long, stop_loss_short)
    }
}

#[cfg(test)]
mod tests {
    use crate::source::{Source, SourceType};
    use crate::{
        BaseLine, BaseStrategy, Confirm, Exit, Pulse, Signal, StopLoss, Strategy, TradeAction,
    };
    use core::Series;
    use timeseries::{BaseTimeSeries, OHLCVSeries};

    struct MockSignal {
        fast_period: usize,
    }

    impl Signal for MockSignal {
        fn lookback(&self) -> usize {
            self.fast_period
        }

        fn trigger(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    struct MockPrimaryConfirm {
        period: usize,
    }

    impl Confirm for MockPrimaryConfirm {
        fn lookback(&self) -> usize {
            self.period
        }

        fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    struct MockSecondaryConfirm {
        period: usize,
    }

    impl Confirm for MockSecondaryConfirm {
        fn lookback(&self) -> usize {
            self.period
        }

        fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
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

        fn filter(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
            (Series::one(len).into(), Series::zero(len).into())
        }

        fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
            (Series::zero(len).into(), Series::one(len).into())
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

        fn close(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            let len = data.len();
            (Series::one(len).into(), Series::zero(len).into())
        }
    }

    #[test]
    fn test_base_strategy_lookback() {
        let strategy = BaseStrategy::new(
            Box::<BaseTimeSeries>::default(),
            Box::new(MockSignal { fast_period: 10 }),
            Box::new(MockPrimaryConfirm { period: 1 }),
            Box::new(MockSecondaryConfirm { period: 1 }),
            Box::new(MockPulse { period: 7 }),
            Box::new(MockBaseLine { period: 15 }),
            Box::new(MockStopLoss {
                period: 2,
                multi: 2.0,
            }),
            Box::new(MockExit {}),
        );
        assert_eq!(strategy.lookback_period, 85);
    }
}
