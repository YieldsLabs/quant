use base::prelude::*;

#[inline]
pub fn source_deserialize(source: usize) -> SourceType {
    match source {
        1 => SourceType::CLOSE,
        2 => SourceType::HL2,
        3 => SourceType::HLC3,
        4 => SourceType::HLCC4,
        5 => SourceType::OHLC4,
        _ => SourceType::CLOSE,
    }
}
