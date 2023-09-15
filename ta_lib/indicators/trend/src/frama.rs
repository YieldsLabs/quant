use core::series::Series;

pub fn frama(high: &[f32], low: &[f32], close: &[f32], period: usize) -> Series<f32> {
    let high = Series::from(high);
    let low = Series::from(low);
    let close = Series::from(close);

    let hh1 = high.highest(2 * period).shift(period);
    let ll1 = low.lowest(2 * period).shift(period);
    let n1 = (hh1 - ll1) / period as f32;

    let hh2 = high.highest(period);
    let ll2 = low.lowest(period);
    let n2 = (hh2 - ll2) / period as f32;

    let hh3 = high.highest(2 * period);
    let ll3 = low.lowest(2 * period);
    let n3 = (hh3 - ll3) / (2 * period) as f32;

    let d = ((n1 + n2).log() - n3.log()) / 2.0_f32.ln();

    let alpha = (-4.6 * (d - 1.0)).exp();

    let frama = close.ew(&alpha.nz(Some(2.0 / (period + 1) as f32)), &close);

    frama
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frama() {
        let high = vec![18.904, 18.988, 18.992, 18.979, 18.941];
        let low = vec![18.825, 18.866, 18.950, 18.912, 18.877];
        let close = vec![18.889, 18.966, 18.963, 18.922, 18.940];
        let expected = vec![18.889, 18.9275, 18.94525, 18.939285, 18.939308];

        let result: Vec<f32> = frama(&high, &low, &close, 3).into();

        assert_eq!(result, expected);
    }
}
