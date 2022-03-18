# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class VerificationBatchExec(models.TransientModel):
    _description = 'Verification Batch Exec'
    _name = 'clv.verification.batch.exec'

    def _default_batch_ids(self):
        return self._context.get('active_ids')
    batch_ids = fields.Many2many(
        comodel_name='clv.verification.batch',
        relation='clv_verification_batch_exec_rel',
        string='Batchs to Execute',
        default=_default_batch_ids)
    count_batches = fields.Integer(
        string='Number of Batchs',
        compute='_compute_count_batches',
        store=False
    )

    @api.depends('batch_ids')
    def _compute_count_batches(self):
        for r in self:
            r.count_batches = len(r.batch_ids)

    def do_verification_batch_exec(self):
        self.ensure_one()

        for batch in self.batch_ids:

            _logger.info(u'%s %s', '>>>>>', batch.name)

            VerificationBatch = self.env['clv.verification.batch']
            VerificationBatch._verification_batch_exec(batch.name)

        return True
