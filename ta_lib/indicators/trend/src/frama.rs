use core::{iff, Series};

pub fn frama(
    high: &Series<f32>,
    low: &Series<f32>,
    close: &Series<f32>,
    period: usize,
) -> Series<f32> {
    let hh1 = high.highest(2 * period).shift(period);
    let ll1 = low.lowest(2 * period).shift(period);
    let n1 = (&hh1 - &ll1) / period as f32;

    let hh2 = high.highest(period);
    let ll2 = low.lowest(period);
    let n2 = (&hh2 - &ll2) / period as f32;

    let hh3 = hh1.max(&hh2);
    let ll3 = ll1.min(&ll2);
    let n3 = (hh3 - ll3) / (2 * period) as f32;

    let d = ((n1 + n2).log() - n3.log()) / 2.0_f32.ln();

    let alpha = iff!(
        d.na(),
        Series::fill(close.len(), 2.0 / (period + 1) as f32),
        (-4.6 * (d - 1.0)).exp()
    );

    close.ew(&alpha, &close)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_frama() {
        let high = Series::from([18.904, 18.988, 18.992, 18.979, 18.941]);
        let low = Series::from([18.825, 18.866, 18.950, 18.912, 18.877]);
        let close = Series::from([18.889, 18.966, 18.963, 18.922, 18.940]);
        let expected = vec![18.889, 18.9275, 18.94525, 18.939285, 18.939308];

        let result: Vec<f32> = frama(&high, &low, &close, 3).into();

        assert_eq!(result, expected);
    }
}
