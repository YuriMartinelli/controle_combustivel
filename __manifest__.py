{
    'name': "Controle de Combustível",

    'summary': "Gestão de abastecimentos e controle de estoque de combustível",

    'description': """
Controle de Combustível
=======================

Sistema completo para gestão de abastecimentos e controle de estoque de combustível.

Funcionalidades principais:
----------------------------
* **Abastecimentos**: Registro de abastecimentos com integração aos veículos/equipamentos da frota
    - Registro de data, hora, hodômetro/horímetro
    - Cálculo automático do valor total (litros × valor/litro)
    - Rastreamento de usuário responsável e motorista
    
* **Estoque de Combustível**: Controle de tanque de 6.000 litros
    - Entradas aumentam o estoque automaticamente
    - Abastecimentos reduzem o estoque
    - Visualização do nível atual do tanque
    - Integração opcional com recebimento de compras
    
* **Permissões por Grupo**:
    - Motorista: registra abastecimentos
    - Analista: acesso a relatórios e visualizações
    - Administrador: acesso total ao módulo
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    'category': 'Operations',
    'version': '1.0',

    'depends': ['base', 'fleet'],

    'data': [
        # Security
        'security/controle_combustivel_security.xml',
        'security/ir.model.access.csv',
        
        # Views
        'views/abastecimento_views.xml',
        'views/estoque_combustivel_views.xml',
        'views/menu.xml',
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}

