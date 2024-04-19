use core::prelude::*;

pub fn wma(source: &Series<f32>, period: usize) -> Series<f32> {
    source.smooth(Smooth::WMA, period)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_wma() {
        let source = Series::from([
            6.5232, 6.5474, 6.5541, 6.5942, 6.5348, 6.4950, 6.5298, 6.5616, 6.5223, 6.5300, 6.5452,
            6.5254, 6.5038, 6.4614, 6.4854, 6.4966, 6.5117, 6.5270, 6.5527, 6.5316,
        ]);
        let period = 3;
        let expected = [
            0.0, 0.0, 6.5467167, 6.573034, 6.557817, 6.5248, 6.5190334, 6.5399, 6.5366497,
            6.5326996, 6.5363164, 6.5327663, 6.5179005, 6.4862, 6.4804664, 6.487, 6.5022836,
            6.516834, 6.5373, 6.5378666,
        ];

        let result: Vec<f32> = wma(&source, period).into();

        assert_eq!(result, expected);
    }
}
