mod candle;
mod cross_ma;
mod ffi;
mod rsi_ma;
mod rsi_two_ma;
mod snatr;
mod testing_ground;

use candle::CandleStrategy;
use cross_ma::CrossMAStrategy;
pub use ffi::*;
use rsi_ma::RSIMAStrategy;
use rsi_two_ma::RSI2xMAStrategy;
use snatr::SNATRStrategy;
use testing_ground::TestingGroundStrategy;
