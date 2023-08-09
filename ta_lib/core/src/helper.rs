use crate::series::Series;

impl Series<f32> {
    pub fn cross_over(&self, rhs: &Series<f32>) -> Series<bool> {
        self.gt(rhs) & self.shift(1).lt(&rhs.shift(1))
    }

    pub fn cross_under(&self, rhs: &Series<f32>) -> Series<bool> {
        self.lt(rhs) & self.shift(1).gt(&rhs.shift(1))
    }

    pub fn cross(&self, rhs: &Series<f32>) -> Series<bool> {
        self.cross_over(rhs) | self.cross_under(rhs)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_cross_over() {
        let a = Series::from([5.5, 5.0, 4.5, 3.0, 2.5]);
        let b = Series::from([4.5, 2.0, 3.0, 3.5, 2.0]);
        let expected: Series<bool> = Series::from([f32::NAN, 0.0, 0.0, 0.0, 1.0]).into();

        let result = a.cross_over(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_cross_under() {
        let a = Series::from([5.5, 5.0, 4.5, 3.0, 2.5]);
        let b = Series::from([4.5, 2.0, 3.0, 3.5, 2.0]);
        let expected: Series<bool> = Series::from([f32::NAN, 0.0, 0.0, 1.0, 0.0]).into();

        let result = a.cross_under(&b);

        assert_eq!(result, expected);
    }

    #[test]
    fn test_cross() {
        let a = Series::from([5.5, 5.0, 4.5, 3.0, 2.5]);
        let b = Series::from([4.5, 2.0, 3.0, 3.5, 2.0]);
        let expected: Series<bool> = Series::from([f32::NAN, 0.0, 0.0, 1.0, 1.0]).into();

        let result = a.cross(&b);

        assert_eq!(result, expected);
    }
}
