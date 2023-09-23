use crate::price::Price;
use crate::{Filter, OHLCVSeries, Signal, StopLoss, Strategy, OHLCV};
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

#[derive(Debug)]
pub struct StopLossLevels {
    pub long: f32,
    pub short: f32,
}

pub struct BaseStrategy {
    data: VecDeque<OHLCV>,
    signal: Box<dyn Signal>,
    filter: Box<dyn Filter>,
    stop_loss: Box<dyn StopLoss>,
    lookback_period: usize,
}

impl BaseStrategy {
    pub fn new(
        signal: Box<dyn Signal>,
        filter: Box<dyn Filter>,
        stop_loss: Box<dyn StopLoss>,
    ) -> Self {
        let lookbacks = [
            signal.lookback(),
            filter.lookback(),
            stop_loss.lookback(),
            DEFAULT_LOOKBACK,
        ];
        let adjusted_lookback = lookbacks.iter().cloned().max().unwrap_or(DEFAULT_LOOKBACK);

        Self {
            data: VecDeque::with_capacity(adjusted_lookback),
            lookback_period: adjusted_lookback,
            signal,
            filter,
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

impl Strategy for BaseStrategy {
    fn next(&mut self, data: OHLCV) -> TradeAction {
        self.store(data);

        if !self.can_process() {
            return TradeAction::DoNothing;
        }

        let series = OHLCVSeries::from_data(&self.data);

        let (go_long_signal, go_short_signal) = self.signal.entry(&series);
        let (exit_long_series, exit_short_series) = self.signal.exit(&series);

        let (go_long_filter, go_short_filter) = self.filter.filter(&series);

        let go_long_series = go_long_signal & go_long_filter;
        let go_short_series = go_short_signal & go_short_filter;

        let go_long = go_long_series.last().unwrap_or_default();
        let go_short = go_short_series.last().unwrap_or_default();

        let exit_long = exit_long_series.last().unwrap_or_default();
        let exit_short = exit_short_series.last().unwrap_or_default();

        let suggested_entry = *series.hlc3().last().unwrap_or(&std::f32::NAN);

        match (go_long, go_short, exit_long, exit_short) {
            (true, _, _, _) => TradeAction::GoLong(suggested_entry),
            (_, true, _, _) => TradeAction::GoShort(suggested_entry),
            (_, _, true, _) => TradeAction::ExitLong,
            (_, _, _, true) => TradeAction::ExitShort,
            _ => TradeAction::DoNothing,
        }
    }

    fn stop_loss(&self) -> StopLossLevels {
        if !self.can_process() {
            return StopLossLevels {
                long: -1.0,
                short: -1.0,
            };
        }

        let series = OHLCVSeries::from_data(&self.data);

        let (stop_loss_long_series, stop_loss_short_series) = self.stop_loss.next(&series);

        let stop_loss_long = stop_loss_long_series.last().unwrap_or_default();
        let stop_loss_short = stop_loss_short_series.last().unwrap_or_default();

        StopLossLevels {
            long: stop_loss_long,
            short: stop_loss_short,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::price::Price;
    use crate::{BaseStrategy, Filter, OHLCVSeries, Signal, StopLoss, Strategy, OHLCV};
    use core::Series;

    struct MockSignal {
        short_period: usize,
    }

    impl Signal for MockSignal {
        fn lookback(&self) -> usize {
            self.short_period
        }

        fn entry(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
            (Series::empty(1), Series::empty(1))
        }

        fn exit(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
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

    struct MockFilter {
        period: usize,
    }

    impl Filter for MockFilter {
        fn lookback(&self) -> usize {
            self.period
        }

        fn filter(&self, _data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
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
            Box::new(MockFilter { period: 1 }),
            Box::new(MockStopLoss {
                period: 2,
                multi: 2.0,
            }),
        );
        assert_eq!(strategy.lookback_period, 55);
    }

    #[test]
    fn test_strategy_data() {
        let mut strategy = BaseStrategy::new(
            Box::new(MockSignal { short_period: 10 }),
            Box::new(MockFilter { period: 1 }),
            Box::new(MockStopLoss {
                period: 2,
                multi: 2.0,
            }),
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
            vec![1.333_333_4, 2.333_333_3, 3.333_333_3, 4.333_333_5]
        );
        assert_eq!(series.hlcc4(), vec![1.375, 2.375, 3.375, 4.375]);
        assert_eq!(series.ohlc4(), vec![1.25, 2.25, 3.25, 4.25]);
    }
}
