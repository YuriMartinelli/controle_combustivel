# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FuelSupply(models.Model):
    _name = 'fuel.supply'
    _description = 'Abastecimento de Combustível'
    _order = 'date desc'

    name = fields.Char(
        string='Referência',
        required=True,
        default='Novo',
        readonly=True,
        copy=False
    )
    
    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Veículo/Equipamento',
        required=True,
        ondelete='restrict',
        help='Veículo ou equipamento que foi abastecido'
    )
    
    date = fields.Datetime(
        string='Data e Hora',
        required=True,
        default=fields.Datetime.now,
        help='Data e hora do abastecimento'
    )
    
    odometer = fields.Float(
        string='Hodômetro/Horímetro',
        help='Leitura do hodômetro (km) ou horímetro (horas) no momento do abastecimento',
        digits=(10, 2)
    )
    
    liters = fields.Float(
        string='Litros',
        required=True,
        digits=(10, 3),
        help='Quantidade de litros abastecidos'
    )
    
    price_unit = fields.Float(
        string='Preço por Litro',
        required=True,
        digits='Product Price',
        help='Valor unitário do litro de combustível'
    )
    
    amount_total = fields.Float(
        string='Total',
        compute='_compute_amount_total',
        store=True,
        digits='Product Price',
        help='Valor total do abastecimento (litros × preço unitário)'
    )
    
    user_id = fields.Many2one(
        'res.users',
        string='Responsável',
        required=True,
        default=lambda self: self.env.user,
        ondelete='restrict',
        help='Usuário que registrou o abastecimento'
    )
    
    driver_id = fields.Many2one(
        'res.users',
        string='Motorista',
        ondelete='restrict',
        help='Motorista que realizou o abastecimento'
    )
    
    notes = fields.Text(
        string='Observações'
    )
    
    state = fields.Selection([
        ('draft', 'Rascunho'),
        ('confirmed', 'Confirmado'),
        ('cancelled', 'Cancelado')
    ], string='Status', default='draft', required=True)
    
    fuel_tank_id = fields.Many2one(
        'fuel.tank',
        string='Tanque',
        ondelete='restrict',
        help='Tanque de onde o combustível foi retirado'
    )
    
    @api.depends('liters', 'price_unit')
    def _compute_amount_total(self):
        """Calcula o valor total multiplicando litros por valor unitário"""
        for record in self:
            record.amount_total = record.liters * record.price_unit
    
    @api.model
    def create(self, vals):
        """Gera sequência automática e verifica/desconta do estoque do tanque"""
        # Gera sequência automática
        if vals.get('name', 'Novo') == 'Novo':
            vals['name'] = self.env['ir.sequence'].next_by_code('fuel.supply') or 'Novo'
        
        # Verifica e desconta do estoque do tanque
        liters = vals.get('liters', 0)
        fuel_tank_id = vals.get('fuel_tank_id')
        
        if fuel_tank_id and liters > 0:
            fuel_tank = self.env['fuel.tank'].browse(fuel_tank_id)
            if fuel_tank.exists():
                # Verifica se há estoque suficiente
                if fuel_tank.current_level < liters:
                    raise ValidationError(
                        f'Estoque insuficiente no tanque "{fuel_tank.name}". '
                        f'Disponível: {fuel_tank.current_level:.2f}L, '
                        f'Necessário: {liters:.2f}L'
                    )
                # Remove o combustível do tanque
                fuel_tank.remove_fuel(liters)
        
        return super(FuelSupply, self).create(vals)
