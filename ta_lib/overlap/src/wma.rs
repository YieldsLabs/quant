use core::series::Series;

pub fn wma(source: &[f64], period: usize) -> Series<f64> {
    let len = source.len();
    let mut wma = Series::empty(len);

    let weight_sum = (period * (period + 1)) as f64 / 2.0;

    let mut sum = 0.0;

    for i in 0..period {
        let weight = (i + 1) as f64;
        sum += source[i] * weight;
    }

    wma[period - 1] = Some(sum / weight_sum);

    for i in period..len {
        sum += (source[i] - source[i - period]) * period as f64 - (weight_sum - period as f64);
        wma[i] = Some(sum / weight_sum);
    }

    wma.nz(Some(0.0))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wma() {
        let source = vec![1.0, 2.0, 3.0, 4.0, 5.0];
        let period = 3;
        let epsilon = 0.001;
        let expected = vec![0.0, 0.0, 2.333333, 3.333333, 4.333333];

        let result = wma(&source, period);

        for i in 0..source.len() {
            assert!(
                (result[i] - expected[i]).abs() < epsilon,
                "at position {}: {} != {}",
                i,
                result[i],
                expected[i]
            )
        }
    }
}
