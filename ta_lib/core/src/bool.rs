use crate::series::Series;

impl Series<f64> {
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
}
