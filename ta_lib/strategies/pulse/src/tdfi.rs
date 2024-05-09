use base::prelude::*;
use core::prelude::*;
use momentum::tdfi;
use timeseries::prelude::*;

const TDFI_UPPER_LINE: f32 = 0.05;
const TDFI_LOWER_LINE: f32 = -0.05;

pub struct TdfiPulse {
    source_type: SourceType,
    smooth_type: Smooth,
    period: usize,
    n: usize,
}

impl TdfiPulse {
    pub fn new(source_type: SourceType, smooth_type: Smooth, period: f32, n: f32) -> Self {
        Self {
            source_type,
            smooth_type,
            period: period as usize,
            n: n as usize,
        }
    }
}

impl Pulse for TdfiPulse {
    fn lookback(&self) -> usize {
        self.period
    }

    fn assess(&self, data: &OHLCVSeries) -> (Series<bool>, Series<bool>) {
        let tdfi = tdfi(
            &data.source(self.source_type),
            self.smooth_type,
            self.period,
            self.n,
        );

        (tdfi.sgt(&TDFI_UPPER_LINE), tdfi.slt(&TDFI_LOWER_LINE))
    }
}

// #[cfg(test)]
// mod tests {
//     use super::*;
//     use std::collections::VecDeque;

//     #[test]
//     fn test_pulse_tdfi() {
//         let pulse = TdfiPulse::new(SourceType::CLOSE, Smooth::TEMA, 6.0, 3.0);
//         let data = VecDeque::from([
//             OHLCV {
//                 ts: 1679825700,
//                 open: 5.993,
//                 high: 6.000,
//                 low: 5.983,
//                 close: 5.997,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679826000,
//                 open: 5.997,
//                 high: 6.001,
//                 low: 5.989,
//                 close: 6.001,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679826300,
//                 open: 6.001,
//                 high: 6.0013,
//                 low: 5.993,
//                 close: 6.007,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679826600,
//                 open: 6.007,
//                 high: 6.008,
//                 low: 5.980,
//                 close: 5.992,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679826900,
//                 open: 5.992,
//                 high: 5.993,
//                 low: 5.976,
//                 close: 5.980,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679827200,
//                 open: 5.980,
//                 high: 5.986,
//                 low: 5.966,
//                 close: 5.969,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679827500,
//                 open: 5.969,
//                 high: 5.969,
//                 low: 5.943,
//                 close: 5.946,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679827800,
//                 open: 5.946,
//                 high: 5.960,
//                 low: 5.939,
//                 close: 5.953,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679828100,
//                 open: 5.953,
//                 high: 5.961,
//                 low: 5.937,
//                 close: 5.939,
//                 volume: 100.0,
//             },
//             OHLCV {
//                 ts: 1679828400,
//                 open: 5.939,
//                 high: 5.945,
//                 low: 5.919,
//                 close: 5.943,
//                 volume: 100.0,
//             },
//         ]);
//         let series = OHLCVSeries::from_data(&data);

//         let (long_signal, short_signal) = pulse.assess(&series);

//         let expected_long_signal = vec![
//             false, true, true, false, false, false, false, false, false, false,
//         ];
//         let expected_short_signal = vec![
//             false, false, false, true, true, true, true, false, false, false,
//         ];

//         let result_long_signal: Vec<bool> = long_signal.into();
//         let result_short_signal: Vec<bool> = short_signal.into();

//         assert_eq!(result_long_signal, expected_long_signal);
//         assert_eq!(result_short_signal, expected_short_signal);
//     }
// }
