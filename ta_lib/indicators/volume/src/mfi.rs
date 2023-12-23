use core::prelude::*;

const ZERO: f32 = 0.0;
const PERCENTAGE_SCALE: f32 = 100.;

pub fn mfi(hlc3: &Series<f32>, volume: &Series<f32>, period: usize) -> Series<f32> {
    let changes = hlc3.change(1);

    let volume_hlc3 = volume * hlc3;

    let positive_volume = changes.sgt(&ZERO) * &volume_hlc3;
    let negative_volume = changes.slt(&ZERO) * &volume_hlc3;

    let upper = positive_volume.sum(period);
    let lower = negative_volume.sum(period);

    let money_ratio = upper / lower;

    let mfi = PERCENTAGE_SCALE - PERCENTAGE_SCALE / (1. + money_ratio);

    mfi.nz(Some(50.))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_mfi() {
        let hlc3 = Series::from([2.0, 2.1666, 2.0, 1.8333, 2.0]);
        let volume = Series::from([1.0, 1.0, 1.0, 1.0, 1.0]);
        let period = 3;
        let epsilon = 0.001;

        let expected = [50.0, 50.0, 51.9992, 36.1106, 34.2859];

        let result: Vec<f32> = mfi(&hlc3, &volume, period).into();

        for i in 0..hlc3.len() {
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
