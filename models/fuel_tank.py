# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FuelTank(models.Model):
    _name = 'fuel.tank'
    _description = 'Tanque de Combustível'
    
    name = fields.Char(
        string='Nome do Tanque',
        required=True,
        help='Identificação do tanque de combustível'
    )
    
    current_level = fields.Float(
        string='Nível Atual (Litros)',
        required=True,
        default=0.0,
        digits=(10, 3),
        help='Quantidade atual de combustível no tanque em litros'
    )
    
    capacity = fields.Float(
        string='Capacidade Total (Litros)',
        required=True,
        default=6000.0,
        digits=(10, 3),
        help='Capacidade máxima do tanque em litros'
    )
    
    available_percentage = fields.Float(
        string='Nível (%)',
        compute='_compute_available_percentage',
        store=True,
        digits=(5, 2),
        help='Percentual do nível atual em relação à capacidade total'
    )
    
    active = fields.Boolean(
        string='Ativo',
        default=True
    )
    
    @api.depends('current_level', 'capacity')
    def _compute_available_percentage(self):
        """Calcula o percentual disponível no tanque"""
        for record in self:
            if record.capacity > 0:
                record.available_percentage = (record.current_level / record.capacity) * 100
            else:
                record.available_percentage = 0.0
    
    @api.constrains('current_level', 'capacity')
    def _check_levels(self):
        """Valida que o nível atual não exceda a capacidade"""
        for record in self:
            if record.current_level < 0:
                raise ValidationError('O nível atual não pode ser negativo.')
            if record.capacity <= 0:
                raise ValidationError('A capacidade do tanque deve ser maior que zero.')
            if record.current_level > record.capacity:
                raise ValidationError(
                    f'O nível atual ({record.current_level:.2f}L) não pode '
                    f'exceder a capacidade do tanque ({record.capacity:.2f}L).'
                )
    
    def add_fuel(self, liters):
        """Adiciona combustível ao tanque (entrada de estoque)"""
        self.ensure_one()
        if liters <= 0:
            raise ValidationError('A quantidade a adicionar deve ser maior que zero.')
        
        new_level = self.current_level + liters
        if new_level > self.capacity:
            raise ValidationError(
                f'Não é possível adicionar {liters:.2f}L. '
                f'O tanque ficaria com {new_level:.2f}L, excedendo a capacidade de {self.capacity:.2f}L.'
            )
        
        self.current_level = new_level
    
    def remove_fuel(self, liters):
        """Remove combustível do tanque (saída para abastecimento)"""
        self.ensure_one()
        if liters <= 0:
            raise ValidationError('A quantidade a remover deve ser maior que zero.')
        
        if self.current_level < liters:
            raise ValidationError(
                f'Estoque insuficiente no tanque "{self.name}". '
                f'Disponível: {self.current_level:.2f}L, Necessário: {liters:.2f}L'
            )
        
        self.current_level -= liters
