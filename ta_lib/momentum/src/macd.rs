use core::series::Series;
use overlap::ema::ema;

pub fn macd(
    source: &[f64],
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
) -> (Series<f64>, Series<f64>, Series<f64>) {
    let ema_fast = ema(source, fast_period);
    let ema_slow = ema(source, slow_period);

    let macd_line = ema_fast - &ema_slow;
    let macd_line_vec: Vec<f64> = macd_line.clone().into();

    let signal_line = ema(&macd_line_vec, signal_period);

    let histogram = &macd_line - &signal_line;

    (macd_line, signal_line, histogram)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_macd() {
        let source = vec![2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0];
        let fast_period = 3;
        let slow_period = 5;
        let signal_period = 4;
        let epsilon = 0.001;
        let expected_macd_line = vec![
            Some(0.0),
            Some(0.33333),
            Some(0.72222),
            Some(1.0648),
            Some(1.334877),
            Some(1.035751),
            Some(0.596751),
            Some(0.184292),
            Some(-0.150576),
            Some(-0.403769),
        ];
        let expected_signal_line = vec![
            Some(0.0),
            Some(0.13333),
            Some(0.36888),
            Some(0.6472),
            Some(0.9223),
            Some(0.9676),
            Some(0.8193),
            Some(0.5653),
            Some(0.2789),
            Some(0.0058),
        ];
        let expected_histogram = vec![
            Some(0.0),
            Some(0.1999),
            Some(0.3533),
            Some(0.4175),
            Some(0.4125),
            Some(0.068),
            Some(-0.2222),
            Some(-0.381),
            Some(-0.4295),
            Some(-0.4096),
        ];

        let (macd_line, signal_line, histogram) =
            macd(&source, fast_period, slow_period, signal_period);

        for i in 0..source.len() {
            match (macd_line[i], expected_macd_line[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!(
                    "at position {}: {:?} != {:?}",
                    i, macd_line[i], expected_macd_line[i]
                ),
            }

            match (signal_line[i], expected_signal_line[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!(
                    "at position {}: {:?} != {:?}",
                    i, signal_line[i], expected_signal_line[i]
                ),
            }

            match (histogram[i], expected_histogram[i]) {
                (Some(a), Some(b)) => {
                    assert!((a - b).abs() < epsilon, "at position {}: {} != {}", i, a, b)
                }
                (None, None) => {}
                _ => panic!(
                    "at position {}: {:?} != {:?}",
                    i, histogram[i], expected_histogram[i]
                ),
            }
        }
    }
}
