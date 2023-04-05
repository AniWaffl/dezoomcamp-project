CREATE TABLE IF NOT EXISTS destorestatistic.events (
    time DateTime,
    type String,
    product_id UInt32,
    category_id UInt32,
    category_code Nullable(String),
    brand Nullable(String),
    price Float32,
    user_id UInt32,
    user_session String,
    datacenter String,
) ENGINE = MergeTree() ORDER BY time;
