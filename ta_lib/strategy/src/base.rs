use price::{average::average_price, median::median_price, typical::typical_price, wcl::wcl};
use std::{
    cmp::min,
    collections::{HashMap, VecDeque},
};

pub struct OHLCV {
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: f64,
}

pub trait Strategy {
    const DEFAULT_LOOKBACK: usize = 55;

    fn next(&mut self, data: OHLCV);
    fn can_process(&self) -> bool;
    fn params(&self) -> HashMap<String, usize>;
}

pub struct BaseStrategy {
    data: VecDeque<OHLCV>,
    lookback_period: usize,
}

impl BaseStrategy {
    pub fn new(lookback_period: usize) -> BaseStrategy {
        let lookback_period = min(lookback_period, Self::DEFAULT_LOOKBACK);

        BaseStrategy {
            data: VecDeque::with_capacity(lookback_period),
            lookback_period,
        }
    }
}

impl Strategy for BaseStrategy {
    fn next(&mut self, data: OHLCV) {
        self.data.push_back(data);

        if self.data.len() > self.lookback_period {
            self.data.pop_front();
        }
    }

    fn can_process(&self) -> bool {
        self.data.len() == self.lookback_period
    }

    fn params(&self) -> HashMap<String, usize> {
        let mut map = HashMap::new();
        map.insert(String::from("lookback_period"), self.lookback_period);

        map
    }
}

pub trait StrategySeries {
    fn open(&self) -> Vec<f64>;
    fn high(&self) -> Vec<f64>;
    fn low(&self) -> Vec<f64>;
    fn close(&self) -> Vec<f64>;
    fn volume(&self) -> Vec<f64>;
    fn hl2(&self) -> Vec<f64>;
    fn hlc3(&self) -> Vec<f64>;
    fn hlcc4(&self) -> Vec<f64>;
    fn ohlc4(&self) -> Vec<f64>;
}

impl StrategySeries for BaseStrategy {
    fn open(&self) -> Vec<f64> {
        self.data.iter().map(|ohlcv| ohlcv.open).collect()
    }

    fn high(&self) -> Vec<f64> {
        self.data.iter().map(|ohlcv| ohlcv.high).collect()
    }

    fn low(&self) -> Vec<f64> {
        self.data.iter().map(|ohlcv| ohlcv.low).collect()
    }

    fn close(&self) -> Vec<f64> {
        self.data.iter().map(|ohlcv| ohlcv.close).collect()
    }

    fn volume(&self) -> Vec<f64> {
        self.data.iter().map(|ohlcv| ohlcv.volume).collect()
    }

    fn hl2(&self) -> Vec<f64> {
        let high = self.high();
        let low = self.low();

        median_price(&high, &low)
    }

    fn hlc3(&self) -> Vec<f64> {
        let high = self.high();
        let low = self.low();
        let close = self.close();

        typical_price(&high, &low, &close)
    }

    fn hlcc4(&self) -> Vec<f64> {
        let high = self.high();
        let low = self.low();
        let close = self.close();

        wcl(&high, &low, &close)
    }

    fn ohlc4(&self) -> Vec<f64> {
        let open = self.open();
        let high = self.high();
        let low = self.low();
        let close = self.close();

        average_price(&open, &high, &low, &close)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_base_strategy_creation() {
        let strategy = BaseStrategy::new(20);
        assert_eq!(strategy.lookback_period, 20);
    }

    #[test]
    fn test_base_strategy_can_process() {
        let mut strategy = BaseStrategy::new(2);
        assert_eq!(strategy.can_process(), false);

        strategy.next(OHLCV {
            open: 1.0,
            high: 2.0,
            low: 1.0,
            close: 2.0,
            volume: 1000.0,
        });
        assert_eq!(strategy.can_process(), false);

        strategy.next(OHLCV {
            open: 2.0,
            high: 3.0,
            low: 2.0,
            close: 3.0,
            volume: 2000.0,
        });
        assert_eq!(strategy.can_process(), true);
    }

    #[test]
    fn test_base_strategy_params() {
        let strategy = BaseStrategy::new(20);
        let params = strategy.params();
        assert_eq!(params.get("lookback_period"), Some(&20));
    }

    #[test]
    fn test_strategy_data() {
        let mut strategy = BaseStrategy::new(3);
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

        assert_eq!(strategy.open(), vec![2.0, 3.0, 4.0]);
        assert_eq!(strategy.high(), vec![3.0, 4.0, 5.0]);
        assert_eq!(strategy.low(), vec![1.5, 2.5, 3.5]);
        assert_eq!(strategy.close(), vec![2.5, 3.5, 4.5]);
        assert_eq!(strategy.volume(), vec![200.0, 300.0, 400.0]);

        assert_eq!(strategy.hl2(), vec![2.25, 3.25, 4.25]);
        assert_eq!(
            strategy.hlc3(),
            vec![2.3333333333333335, 3.3333333333333335, 4.333333333333333]
        );
        assert_eq!(strategy.hlcc4(), vec![2.375, 3.375, 4.375]);
        assert_eq!(strategy.ohlc4(), vec![2.25, 3.25, 4.25]);
    }
}
