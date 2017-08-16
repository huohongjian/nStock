

DROP TABLE IF EXISTS ts_hist_data;
CREATE TABLE ts_hist_data
(
    id   serial PRIMARY KEY,
    date date,
    code text,
    open double precision,
    high double precision,
    close double precision,
    low double precision,
    volume double precision,
    price_change double precision,
    p_change double precision,
    ma5 double precision,
    ma10 double precision,
    ma20 double precision,
    v_ma5 double precision,
    v_ma10 double precision,
    v_ma20 double precision,
    turnover double precision,
    qfq double precision,
    hfq double precision,
    ispeak boolean,
    isbott boolean
) WITH (OIDS=FALSE);
-- ALTER TABLE ts_hist_data OWNER TO hhj;
CREATE INDEX ix_data_hist_code ON ts_hist_data USING btree (code);
CREATE INDEX ix_data_hist_date ON ts_hist_data USING btree (date);
CREATE INDEX ix_data_hist_hfq ON ts_hist_data USING btree (hfq);
CREATE INDEX ix_data_hist_qfq ON ts_hist_data USING btree (qfq);
CREATE INDEX ix_data_hist_ispeak ON ts_hist_data USING btree (ispeak);
CREATE INDEX ix_data_hist_isbott ON ts_hist_data USING btree (isbott);


--delete from ts_hist_data where date='2015-02-24';

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

DROP TABLE IF EXISTS stock_list;
CREATE TABLE stock_list (
    id      serial PRIMARY KEY,
    code    text,
    name    text,
    industry text,
    concept text,
    area    text,
    al    boolean NOT NULL DEFAULT true,
    sh    boolean NOT NULL DEFAULT false,
    sz    boolean NOT NULL DEFAULT false,
    st    boolean NOT NULL DEFAULT false,
    zxb   boolean NOT NULL DEFAULT false,
    cyb   boolean NOT NULL DEFAULT false,
    hssb  boolean NOT NULL DEFAULT false,
    szwl  boolean NOT NULL DEFAULT false,
    tradable boolean NOT NULL DEFAULT false,
    hold  boolean NOT NULL DEFAULT false,
    jjcg  boolean NOT NULL DEFAULT false,
    yxg   boolean NOT NULL DEFAULT false,
    gzg   boolean NOT NULL DEFAULT false,
    zxg   boolean NOT NULL DEFAULT false,
    ccg   boolean NOT NULL DEFAULT false
) WITH (OIDS=FALSE);
--DROP INDEX IF EXISTS ix_stock_list_code;
CREATE INDEX ix_stock_list_code     ON stock_list USING btree (code);
CREATE INDEX ix_stock_list_industry ON stock_list USING btree (industry);
CREATE INDEX ix_stock_list_concept  ON stock_list USING btree (concept);
CREATE INDEX ix_stock_list_area     ON stock_list USING btree (area);
CREATE INDEX ix_stock_list_al       ON stock_list USING btree (al);
CREATE INDEX ix_stock_list_tradable ON stock_list USING btree (tradable);
CREATE INDEX ix_stock_list_hold     ON stock_list USING btree (hold);
CREATE INDEX ix_stock_list_jjcg     ON stock_list USING btree (jjcg);
CREATE INDEX ix_stock_list_yxg      ON stock_list USING btree (yxg);
CREATE INDEX ix_stock_list_gzg      ON stock_list USING btree (gzg);
CREATE INDEX ix_stock_list_zxg      ON stock_list USING btree (zxg);
CREATE INDEX ix_stock_list_ccg      ON stock_list USING btree (ccg);

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





