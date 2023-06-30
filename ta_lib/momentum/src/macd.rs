use overlap::ema::ema;

pub fn macd(
    data: &[f64],
    fast_period: usize,
    slow_period: usize,
    signal_period: usize,
) -> (Vec<Option<f64>>, Vec<Option<f64>>, Vec<Option<f64>>) {
    let ema_fast = ema(data, fast_period);
    let ema_slow = ema(data, slow_period);

    let macd_line = ema_fast
        .iter()
        .zip(&ema_slow)
        .map(|(&fast, &slow)| match (fast, slow) {
            (Some(fast), Some(slow)) => Some(fast - slow),
            _ => None,
        })
        .collect::<Vec<_>>();

    let signal_line_values = ema(
        &macd_line.iter().filter_map(|&x| x).collect::<Vec<_>>(),
        signal_period,
    );

    let mut signal_line = vec![None; macd_line.len() - signal_line_values.len()];
    signal_line.extend(signal_line_values);

    let histogram = macd_line
        .iter()
        .zip(&signal_line)
        .map(|(&macd, &signal)| match (macd, signal) {
            (Some(macd), Some(signal)) => Some(macd - signal),
            _ => None,
        })
        .collect::<Vec<_>>();

    (macd_line, signal_line, histogram)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_macd() {
        let data = vec![2.0, 4.0, 6.0, 8.0, 10.0, 9.0, 8.0, 7.0, 6.0, 5.0];
        let fast_period = 3;
        let slow_period = 5;
        let signal_period = 4;
        let epsilon = 0.001;
        let expected_macd_line = vec![
            None,
            None,
            None,
            None,
            Some(1.334877),
            Some(1.035751),
            Some(0.596751),
            Some(0.184292),
            Some(-0.150576),
            Some(-0.403769),
        ];
        let expected_signal_line = vec![
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            Some(0.654418),
            Some(0.332421),
            Some(0.037945),
        ];
        let expected_histogram = vec![
            None,
            None,
            None,
            None,
            None,
            None,
            None,
            Some(-0.470126),
            Some(-0.482997),
            Some(-0.441714),
        ];

        let (macd_line, signal_line, histogram) =
            macd(&data, fast_period, slow_period, signal_period);

        for i in 0..data.len() {
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
