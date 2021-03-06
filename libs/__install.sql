/*
DROP TABLE IF EXISTS st_dictionary;
CREATE TABLE st_dictionary
(
  id      serial PRIMARY KEY,
  key     text,
  value   text
) WITH (OIDS=FALSE);
CREATE INDEX ix_st_dictionary_key  ON st_dictionary USING btree (key);
INSERT INTO st_dictionary (key, value) VALUES 
('renew_ts_trade_cal',  '获取交易日数据，并保存至[ts_trade_cal]表'),
('renew_ts_basics',     '获取全部股票的基本信息，并保存至[ts_basics]表'),
('renew_ts_today_all',  '获取股票的实时交易数据，并保存至表[ts_today_all]');


DROP TABLE IF EXISTS st_log;
CREATE TABLE st_log
(
  id      serial PRIMARY KEY,
  dtime   timestamp(0) without time zone NOT NULL DEFAULT now(),
  dowork  text,
  remark  text
) WITH (OIDS=FALSE);
CREATE INDEX ix_st_log_dtime  ON st_log USING btree (dtime);
CREATE INDEX ix_st_log_dowork ON st_log USING btree (dowork);


DROP TABLE IF EXISTS st_k_data;
CREATE TABLE st_k_data
(
    id      serial PRIMARY KEY,
    date    date,
    code    text,
    open    double precision,
    close   double precision,
    high    double precision,
    low     double precision,
    settle  double precision,
    change  double precision,
    amount  double precision,
    volume  double precision,
    turn    double precision,
    peak    boolean,
    bott    boolean
) WITH (OIDS=FALSE);
-- ALTER TABLE ts_hist_data OWNER TO hhj;
CREATE INDEX ix_st_k_data_code ON st_k_data USING btree (code);
CREATE INDEX ix_st_k_data_date ON st_k_data USING btree (date);
CREATE INDEX ix_st_k_data_peak ON st_k_data USING btree (peak);
CREATE INDEX ix_st_k_data_bott ON st_k_data USING btree (bott);
*/



DROP TABLE IF EXISTS st_hist_data;
DROP SEQUENCE IF EXISTS st_hist_data_seq;
CREATE SEQUENCE st_hist_data_seq;
CREATE TABLE st_hist_data
(
    id   		bigint NOT NULL DEFAULT nextval('st_hist_data_seq') PRIMARY KEY,
    date 		date,
    code 		text,
    open 		double precision,
    close           double precision,
    high            double precision,
    low             double precision,
    yest            double precision,
    price_change    double precision,
    p_change 		double precision,
    volume          double precision,
    amount          double precision,
    ma5             double precision,
    ma10            double precision,
    ma20            double precision,
    v_ma5           double precision,
    v_ma10          double precision,
    v_ma20          double precision,
    turnover        double precision,
    qfq             double precision,
    hfq             double precision,
    peak            integer NOT NULL DEFAULT -1,
    bott            integer NOT NULL DEFAULT -1,
    CONSTRAINT  code_date UNIQUE (code, date) 
) WITH (OIDS=FALSE);
--CREATE INDEX ix_st_hist_data_code 	ON st_hist_data USING btree (code);
CREATE INDEX ix_st_hist_data_date 	ON st_hist_data USING btree (code);
CREATE INDEX ix_st_hist_data_peak 	ON st_hist_data USING btree (peak);
CREATE INDEX ix_st_hist_data_bott 	ON st_hist_data USING btree (bott);


----------------------------------------------------------------
/*
DROP TABLE data_realtime;
DROP SEQUENCE IF EXISTS data_realtime_seq;
CREATE SEQUENCE data_realtime_seq;
CREATE TABLE data_realtime
(
  id bigint NOT NULL DEFAULT nextval('data_realtime_seq'),
  date date,
  time time,
  code text,
  open double precision,
  pre_close double precision,
  price double precision,
  high double precision,
  low double precision,
  bid double precision,
  ask double precision,
  volume double precision,
  amount double precision,
  b1_v double precision,
  b1_p double precision,
  b2_v double precision,
  b2_p double precision,
  b3_v double precision,
  b3_p double precision,
  b4_v double precision,
  b4_p double precision,
  b5_v double precision,
  b5_p double precision,
  a1_v double precision,
  a1_p double precision,
  a2_v double precision,
  a2_p double precision,
  a3_v double precision,
  a3_p double precision,
  a4_v double precision,
  a4_p double precision,
  a5_v double precision,
  a5_p double precision
) WITH (OIDS=FALSE);
ALTER TABLE data_realtime OWNER TO hhj;
CREATE INDEX ix_data_realtime_id ON data_realtime USING btree (id);
CREATE INDEX ix_data_realtime_date ON data_realtime USING btree (date);
CREATE INDEX ix_data_realtime_time ON data_realtime USING btree (time);
CREATE INDEX ix_data_realtime_code ON data_realtime USING btree (code);
*/
----------------------------------------------------------------
/*
DROP TABLE IF EXISTS st_basics;
CREATE TABLE st_basics (
    id                  serial PRIMARY KEY,
    code                text UNIQUE,-- 代码
    name                text,		-- 名称
    area                text,		-- 地区
    industry            text,		-- 所属行业
    pe                  real,		-- 市盈率
    outstanding         real,		-- 流通股本（亿）
    totals              real,		-- 总股本（亿）
    totalAssets         real,		-- 总资产（万）
    liquidAssets        real,		-- 流动资产
    fixedAssets	        real,		-- 固定资产
    reserved            real,       -- 公积金
    reservedPerShare    real,       -- 每股公积金
    esp                 real,       -- 每股收益
    bvps                real,		-- 每股净资
    pb                  real, 		-- 市净率
    timeToMarket        integer,	-- 上市日期
    undp                real,		-- 未分配利润
    perundp             real,		-- 每股未分配利润
    rev                 real,		-- 收入同比
    profit              real,		-- 利润同比
    gpr                 real,       -- 毛利率
    npr                 real,       -- 净利润率
    holders             integer,    -- 股东人数

    al   	boolean NOT NULL DEFAULT true,
    sh		boolean NOT NULL DEFAULT false,
    sz		boolean NOT NULL DEFAULT false,
    st    	boolean NOT NULL DEFAULT false,
    zxb   	boolean NOT NULL DEFAULT false,
    cyb   	boolean NOT NULL DEFAULT false,
    hssb  boolean NOT NULL DEFAULT false,

    szwl  boolean NOT NULL DEFAULT false,
    jjcg  boolean NOT NULL DEFAULT false,
    yxg   boolean NOT NULL DEFAULT false,
    gzg   boolean NOT NULL DEFAULT false,
    zxg   boolean NOT NULL DEFAULT false,
    ccg   boolean NOT NULL DEFAULT false
) WITH (OIDS=FALSE);
CREATE INDEX ix_st_basics_code 	ON st_basics USING btree (code);

*/
-----------------------------------------------------------------
/*
DROP TABLE IF EXISTS profit;
CREATE TABLE profit
(
    id   serial PRIMARY KEY,
    code text NOT NULL DEFAULT '',
    name text NOT NULL DEFAULT '',
    pc double precision,
    np double precision,
    hp double precision,
    lp double precision,
    nhr double precision,
    lhr double precision,
    nlr double precision,
    pks int,
    bts int,
    pds int,
    bds int,
    pe double precision,
    pb double precision,
    esp double precision,
    bvps double precision,
    outs double precision,
    tots double precision,
    vol double precision,
    turn double precision,
    industry text NOT NULL DEFAULT '',
    concept text NOT NULL DEFAULT '',
    area    text NOT NULL DEFAULT '',
    market  date
) WITH (OIDS=FALSE);
ALTER TABLE profit OWNER TO hhj;
CREATE INDEX ix_profit_code ON profit USING btree (code);
*/
-------------------------------------------------------
/*
DROP TABLE IF EXISTS stock_zxg;
CREATE TABLE stock_zxg
(
    date date default current_date,
    code text,
    reason text
) WITH (OIDS=FALSE);
ALTER TABLE stock_zxg OWNER TO hhj;
CREATE INDEX ix_stock_zxg_code ON stock_zxg USING btree (code COLLATE pg_catalog."default");
CREATE INDEX ix_stock_zxg_date ON stock_zxg USING btree (date);
*/
---------------------------------------------------------
/*
DROP TABLE IF EXISTS stock_fund_holdings;
CREATE TABLE stock_fund_holdings
(
    code text,
    name text,
    date date,
    nums int,
    nlast int,
    count double precision,
    clast double precision,
    amount double precision,
    ratio double precision
) WITH (OIDS=FALSE);
ALTER TABLE stock_fund_holdings OWNER TO hhj;
CREATE INDEX ix_stock_fund_holdings_code ON stock_fund_holdings USING btree (code);
CREATE INDEX ix_stock_fund_holdings_date ON stock_fund_holdings USING btree (date);
CREATE INDEX ix_stock_fund_holdings_amount ON stock_fund_holdings USING btree (amount);
CREATE INDEX ix_stock_fund_holdings_ratio ON stock_fund_holdings USING btree (ratio);
*/
--------------------------------------------------------
/*
DROP TABLE IF EXISTS stock_fetch_log;
DROP SEQUENCE IF EXISTS stock_fetch_log_seq;
CREATE SEQUENCE stock_fetch_log_seq;
CREATE TABLE stock_fetch_log
(
    id integer NOT NULL DEFAULT nextval('stock_fetch_log_seq'),
    code text,
    fetchdate date
) WITH (OIDS=FALSE);
CREATE INDEX ix_stock_fetch_log_code ON stock_fetch_log USING btree (code);
*/

--------------------------------------------------------
/*
DROP TABLE IF EXISTS trade;
CREATE TABLE trade
(
    id      serial PRIMARY KEY,
    code    text,
    bprice  double      precision DEFAULT 0,
    bamount integer     DEFAULT 0,
    cost    double      precision DEFAULT 0,    --总成本
    bdate   timestamp   DEFAULT now(),
    sprice  double      precision DEFAULT 0,
    samount integer     DEFAULT 0,
    income  double      precision DEFAULT 0,    --净收入
    sdate   timestamp   DEFAULT now(),
    position integer    DEFAULT 0,              --头寸
    profit  double      precision DEFAULT 0     --盈利
) WITH (OIDS=FALSE);
ALTER TABLE trade OWNER TO hhj;
CREATE INDEX ix_trade_code ON trade USING btree (code);
CREATE INDEX ix_trade_position ON trade USING btree (position);
*/
--------------------------------------------------------





