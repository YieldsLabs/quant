use shared::StochType;

pub fn map_to_stoch(stoch_type: usize) -> StochType {
    match stoch_type {
        1 => StochType::STOCHOSC,
        _ => StochType::STOCHOSC,
    }
}
