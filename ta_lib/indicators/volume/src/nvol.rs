use core::prelude::*;

pub fn nvol(volume: &Series<f32>, smooth_type: Smooth, period: usize) -> Series<f32> {
    SCALE * volume / volume.smooth(smooth_type, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_nvol() {
        let volume = Series::from([528.0, 69.0, 136.0, 78.0, 353.0, 59.0]);
        let period = 2;

        let expected = [100.0, 23.115578, 132.68292, 72.897194, 163.8051, 28.640778];

        let result: Vec<f32> = nvol(&volume, Smooth::SMA, period).into();

        assert_eq!(result, expected);
    }
}
