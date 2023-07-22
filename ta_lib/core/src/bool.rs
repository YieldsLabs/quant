use crate::series::Series;

impl Series<f64> {
    fn compare_series<F>(&self, rhs: &Series<f64>, f: F) -> Series<bool>
    where
        F: Fn(f64, f64) -> bool,
    {
        self.zip_with(rhs, |a, b| match (a, b) {
            (Some(a_val), Some(b_val)) => Some(f(*a_val, *b_val)),
            _ => None,
        })
    }

    fn compare<F>(&self, scalar: f64, f: F) -> Series<bool>
    where
        F: Fn(f64, f64) -> bool,
    {
        self.fmap(|x| x.map(|v| f(*v, scalar)))
    }

    pub fn eq(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a == b)
    }

    pub fn ne(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a != b)
    }

    pub fn gt(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a > b)
    }

    pub fn gte(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a >= b)
    }

    pub fn lt(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a < b)
    }

    pub fn lte(&self, scalar: f64) -> Series<bool> {
        self.compare(scalar, |a, b| a <= b)
    }

    pub fn eq_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a == b)
    }

    pub fn ne_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a != b)
    }

    pub fn gt_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a > b)
    }

    pub fn gte_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a >= b)
    }

    pub fn lt_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a < b)
    }

    pub fn lte_series(&self, rhs: &Series<f64>) -> Series<bool> {
        self.compare_series(rhs, |a, b| a <= b)
    }
}
