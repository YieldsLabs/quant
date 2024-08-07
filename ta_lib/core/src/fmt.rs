use crate::series::Series;
use std::fmt;

impl<T: fmt::Display> fmt::Display for Series<T> {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "[")?;
        for (i, item) in self.iter().enumerate() {
            if i > 0 {
                write!(f, ", ")?;
            }
            match item {
                Some(value) => write!(f, "{}", value)?,
                None => write!(f, "None")?,
            }
        }
        write!(f, "]")
    }
}
