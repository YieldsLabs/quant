use core::Series;

pub fn obv(
    source: &Series<f32>,
    volume: &Series<f32>,
    period: usize,
    smoothing: Option<&str>,
) -> Series<f32> {
    let obv = (source.change(1).nz(Some(0.0)).sign() * volume).cumsum();

    match smoothing {
        Some("WMA") => obv.wma(period),
        Some("EMA") => obv.ema(period),
        Some("SMMA") => obv.smma(period),
        Some("SMA") | _ => obv.ma(period),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_obv() {
        let close = Series::from([
            7.7975, 7.8065, 7.817, 7.831, 7.82, 7.826, 7.837, 7.844, 7.8655,
        ]);

        let volume = Series::from([
            3798.0, 5415.0, 7110.0, 2172.0, 7382.0, 2755.0, 2130.0, 21988.0, 9441.0,
        ]);

        let period = 3;

        let expected = [
            3798.0, 6505.5, 9778.0, 14677.0, 15310.333, 14492.0, 13659.667, 22617.334, 33803.668,
        ];

        let result: Vec<f32> = obv(&close, &volume, period, Some("SMA")).into();

        assert_eq!(result, expected);
    }
}
