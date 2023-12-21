use crate::series::Series;
use crate::traits::{Comparator, Cross};

impl Cross<f32> for Series<f32> {
    type Output = Series<bool>;

    fn cross_over(&self, line: &f32) -> Self::Output {
        self.sgt(line) & self.shift(1).slt(line)
    }

    fn cross_under(&self, line: &f32) -> Self::Output {
        self.slt(line) & self.shift(1).sgt(line)
    }

    fn cross(&self, line: &f32) -> Self::Output {
        self.cross_over(line) | self.cross_under(line)
    }
}

impl Cross<Series<f32>> for Series<f32> {
    type Output = Series<bool>;

    fn cross_over(&self, rhs: &Series<f32>) -> Self::Output {
        self.sgt(rhs) & self.shift(1).slt(&rhs.shift(1))
    }

    fn cross_under(&self, rhs: &Series<f32>) -> Self::Output {
        self.slt(rhs) & self.shift(1).sgt(&rhs.shift(1))
    }

    fn cross(&self, rhs: &Series<f32>) -> Self::Output {
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
