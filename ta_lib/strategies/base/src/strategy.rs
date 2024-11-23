use crate::source::{Source, SourceType};
use crate::{BaseLine, Confirm, Exit, Pulse, Signal, Strategy};
use core::prelude::*;
use timeseries::prelude::*;

const DEFAULT_LOOKBACK: Period = 16;

#[derive(Debug, PartialEq)]
pub enum TradeAction {
    GoLong(Scalar),
    GoShort(Scalar),
    ExitLong(Scalar),
    ExitShort(Scalar),
    DoNothing,
}

pub struct BaseStrategy {
    timeseries: Box<dyn TimeSeries>,
    signal: Box<dyn Signal>,
    confirm: Box<dyn Confirm>,
    pulse: Box<dyn Pulse>,
    base_line: Box<dyn BaseLine>,
    exit: Box<dyn Exit>,
    lookback_period: usize,
}

impl BaseStrategy {
    pub fn new(
        timeseries: Box<dyn TimeSeries>,
        signal: Box<dyn Signal>,
        confirm: Box<dyn Confirm>,
        pulse: Box<dyn Pulse>,
        base_line: Box<dyn BaseLine>,
        exit: Box<dyn Exit>,
    ) -> Self {
        let lookbacks = [
            signal.lookback(),
            confirm.lookback(),
            pulse.lookback(),
            base_line.lookback(),
            exit.lookback(),
            DEFAULT_LOOKBACK,
        ];
        let lookback_period = lookbacks.into_iter().max().unwrap_or(DEFAULT_LOOKBACK);

        Self {
            timeseries,
            signal,
            confirm,
            pulse,
            base_line,
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
        let theo_price = self.suggested_entry(&ohlcv, bar_index);

        match self.trade_signals(&ohlcv, bar_index) {
            (true, _, _, _) => TradeAction::GoLong(theo_price),
            (_, true, _, _) => TradeAction::GoShort(theo_price),
            (_, _, true, _) => TradeAction::ExitLong(theo_price),
            (_, _, _, true) => TradeAction::ExitShort(theo_price),
            _ => TradeAction::DoNothing,
        }
    }
}

impl BaseStrategy {
    fn trade_signals(&self, ohlcv: &OHLCVSeries, bar_index: usize) -> (bool, bool, bool, bool) {
        let (signal_go_long, signal_go_short) = self.signal.trigger(ohlcv);

        let (baseline_confirm_long, baseline_confirm_short) = self.base_line.filter(ohlcv);
        let (primary_confirm_long, primary_confirm_short) = self.confirm.filter(ohlcv);
        let (pulse_confirm_long, pulse_confirm_short) = self.pulse.assess(ohlcv);

        let (exit_close_long, exit_close_short) = self.exit.close(ohlcv);
        let (baseline_close_long, baseline_close_short) = self.base_line.close(ohlcv);

        let confirm_long = primary_confirm_long & pulse_confirm_long;
        let confirm_short = primary_confirm_short & pulse_confirm_short;

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

    fn suggested_entry(&self, ohlcv: &OHLCVSeries, bar_index: usize) -> Scalar {
        ohlcv
            .source(SourceType::CLOSE)
            .get(bar_index)
            .unwrap_or(NAN)
    }
}

#[cfg(test)]
mod tests {
    use crate::{BaseLine, BaseStrategy, Confirm, Exit, Pulse, Signal};
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

    struct MockConfirm {
        period: usize,
    }

    impl Confirm for MockConfirm {
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
            Box::new(MockConfirm { period: 1 }),
            Box::new(MockPulse { period: 7 }),
            Box::new(MockBaseLine { period: 15 }),
            Box::new(MockExit {}),
        );
        assert_eq!(strategy.lookback_period, 16);
    }
}
