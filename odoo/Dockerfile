FROM camptocamp/odoo-project:10.0-2.1.1
MAINTAINER Camptocamp

# Install additional debian packages if needed
# RUN set -x; \
#         apt-get update \
#         && apt-get install -y --no-install-recommends \
#         python-shapely \
#         && apt-get clean \
#         && rm -rf /var/lib/apt/lists/*

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
  /opt/odoo/external-src/l10n-switzerland, \
  /opt/odoo/external-src/partner-contact, \
  /opt/odoo/external-src/project, \
  /opt/odoo/local-src," \
  LIMIT_TIME_CPU=86400 \
  LIMIT_TIME_REAL=86400 \
  LIMIT_MEMORY_SOFT=1342177280 \
  LIMIT_MEMORY_HARD=1610612736
