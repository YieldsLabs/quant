use core::series::Series;

pub fn macd(
    source: &[f64],
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
) -> (Vec<f64>, Vec<f64>, Vec<f64>) {
    let source = Series::from(source);

    let ema_fast = source.ema(fast_period);
    let ema_slow = source.ema(slow_period);

    let macd_line = ema_fast - &ema_slow;

    let signal_line = macd_line.ema(signal_period);

    let histogram = &macd_line - &signal_line;

    (macd_line.into(), signal_line.into(), histogram.into())
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
            0.0, 0.33333, 0.72222, 1.0648, 1.334877, 1.035751, 0.596751, 0.184292, -0.150576,
            -0.403769,
        ];
        let expected_signal_line = vec![
            0.0, 0.13333, 0.36888, 0.6472, 0.9223, 0.9676, 0.8193, 0.5653, 0.2789, 0.0058,
        ];
        let expected_histogram = vec![
            0.0, 0.1999, 0.3533, 0.4175, 0.4125, 0.068, -0.2222, -0.381, -0.4295, -0.4096,
        ];

        let (macd_line, signal_line, histogram) =
            macd(&source, fast_period, slow_period, signal_period);

        for i in 0..source.len() {
            assert!(
                (macd_line[i] - expected_macd_line[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                macd_line[i],
                expected_macd_line[i]
            );

            assert!(
                (signal_line[i] - expected_signal_line[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                signal_line[i],
                expected_signal_line[i]
            );

            assert!(
                (histogram[i] - expected_histogram[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                histogram[i],
                expected_histogram[i]
            );
        }
    }
}
