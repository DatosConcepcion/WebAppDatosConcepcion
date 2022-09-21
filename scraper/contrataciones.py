from urllib.parse import urlsplit, parse_qs

import scrapy
import pandas as pd


base_url = "https://cdeluruguay.gob.ar/datagov"


class ContratacionesConcepcionSpider(scrapy.Spider):
    name = "contrataciones-concepcion-spider"
    start_urls = [f"{base_url}/proveedoresContratados.php"]

    def parse(self, response):
        last_update_date = (
            response.xpath(
                "//table//table/tr[contains(.,'Fecha última actualización')]"
            )
            .xpath("td[@class='textoTablaReporte']/text()")
            .get()
        )
        print(last_update_date)

        start_date = "2009-01-01"
        end_date = last_update_date  # FIXME!

        for date in pd.date_range(start_date, end_date, freq="M"):
            yield scrapy.Request(
                url=f"{base_url}/proveedoresContratadosAMR.php?anio={date.year}&mes={date.month}",  # noqa: E501
                callback=self.parse_by_month,
            )

    def parse_by_month(self, response):
        market_ids = response.xpath(
            "//table[contains(@align, 'left')]/tr/td[1]/text()"
        ).getall()[1:]
        market_names = response.xpath(
            "//table[contains(@align, 'left')]/tr/td[2]/text()"
        ).getall()[1:]
        market_urls = response.xpath(
            "//a[contains(@title, 'Ver desagregado por proveedores')]/@href"
        ).getall()

        for url, id, name in zip(market_urls, market_ids, market_names):
            yield response.follow(
                url=url,
                callback=self.parse_by_market,
                cb_kwargs={"market_id": id, "market_name": name},
            )

    def parse_by_market(self, response, market_id: str, market_name: str):
        query = urlsplit(response.url).query
        params = parse_qs(query)

        # Fix columns names
        df = pd.read_html(response.text)[1]
        columns = ["_".join(c.lower().split()) for c in df.iloc[0].to_list()]
        columns = [c if c != "cuil_proveedor" else "cuil" for c in columns]
        df.columns = columns
        df = df.drop(
            [
                "porcentaje_cantidad",
                "porcentaje_importe",
            ],
            axis=1,
        )

        # Fix number
        df.importe = df.importe.apply(
            lambda ele: str(ele).replace(".", "").replace(",", ".")
        )

        for row in df.to_dict("records")[1:]:
            yield {
                "año": params["anio"][0],
                "mes": params["mes"][0],
                "rubro_id": market_id,
                "rubro": market_name,
                **row,
            }
