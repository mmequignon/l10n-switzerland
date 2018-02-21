FROM camptocamp/odoo-project:10.0-2.4.1
MAINTAINER Camptocamp

# Install additional debian packages if needed
# RUN set -x; \
#         apt-get update \
#         && apt-get install -y --no-install-recommends \
#         python-shapely \
#         && apt-get clean \
#         && rm -rf /var/lib/apt/lists/*

COPY ./before-migrate-entrypoint.d/* odoo/before-migrate-entrypoint.d/
COPY ./start-entrypoint.d/* odoo/start-entrypoint.d/
RUN chmod +x odoo/before-migrate-entrypoint.d/* \
    && chmod +x odoo/start-entrypoint.d/*

# Install additional python packages if needed
COPY ./requirements.txt /opt/odoo
RUN cd /opt/odoo && pip install -r requirements.txt

ENV ADDONS_PATH="/opt/odoo/external-src/server-tools, \
  /opt/odoo/src/addons, \
  /opt/odoo/external-src/odoo-cloud-platform, \
  /opt/odoo/external-src/account-financial-tools, \
  /opt/odoo/external-src/account-financial-reporting, \
  /opt/odoo/external-src/web, \
  /opt/odoo/external-src/reporting-engine, \
  /opt/odoo/external-src/bank-payment, \
  /opt/odoo/external-src/bank-statement-import, \
  /opt/odoo/external-src/l10n-switzerland, \
  /opt/odoo/external-src/partner-contact, \
  /opt/odoo/external-src/project, \
  /opt/odoo/external-src/hr, \
  /opt/odoo/local-src," \
  LIMIT_TIME_CPU=86400 \
  LIMIT_TIME_REAL=86400 \
  LIMIT_MEMORY_SOFT=1342177280 \
  LIMIT_MEMORY_HARD=1610612736
