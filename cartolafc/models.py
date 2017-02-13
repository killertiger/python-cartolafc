# -*- coding: utf-8 -*-
from datetime import datetime


class BaseModel(object):
    """ Base class from which all Cartola FC models will inherit. """

    def __init__(self, param_defaults, **kwargs):
        for param in param_defaults:
            setattr(self, param, kwargs.get(param, getattr(self, param, None)))

    @classmethod
    def from_dict(cls, data, extra=None):
        """
        Create a new instance based on a JSON dict. Any kwargs should be supplied by the inherited, calling class.
        Args:
            data: A JSON dict, as converted from the JSON in the Cartola FC API.
        """

        json_data = data.copy()
        return cls(**json_data)


class Club(BaseModel):
    def __init__(self, **kwargs):
        param_defaults = ('id', 'nome', 'abreviacao', 'posicao', 'escudos')
        super(Club, self).__init__(param_defaults, **kwargs)


class Highlight(BaseModel):
    def __init__(self, **kwargs):
        param_defaults = ('atleta', 'escalacoes', 'clube', 'escudo_clube', 'posicao')
        super(Highlight, self).__init__(param_defaults, **kwargs)

    @classmethod
    def from_dict(cls, data, extra=None):
        data['atleta'] = Player.from_dict(data.pop('Atleta'))
        return super(cls, cls).from_dict(data)


class Match(BaseModel):
    def __init__(self, **kwargs):
        param_defaults = ('clube_casa', 'clube_casa_posicao', 'clube_visitante', 'clube_visitante_posicao',
                          'partida_data', 'local')
        super(Match, self).__init__(param_defaults, **kwargs)

    @classmethod
    def from_dict(cls, data, extra=None):
        data['clube_casa'] = Club.from_dict(extra[str(data.pop('clube_casa_id'))])
        data['clube_visitante'] = Club.from_dict(extra[str(data.pop('clube_visitante_id'))])
        return super(cls, cls).from_dict(data)


class Player(BaseModel):
    def __init__(self, **kwargs):
        param_defaults = ('atleta_id', 'nome', 'apelido', 'foto', 'preco_editorial')
        super(Player, self).__init__(param_defaults, **kwargs)


class Round(BaseModel):
    def __init__(self, **kwargs):
        param_defaults = ('rodada_id', 'inicio', 'fim')
        super(Round, self).__init__(param_defaults, **kwargs)

    @classmethod
    def from_dict(cls, data, extra=None):
        date_format = '%Y-%m-%d %H:%M:%S'
        data['inicio'] = datetime.strptime(data['inicio'], date_format)
        data['fim'] = datetime.strptime(data['fim'], date_format)
        return super(cls, cls).from_dict(data)


class Sponsor(BaseModel):
    def __init__(self, **kwargs):
        param_defaults = ('liga_editorial_id', 'liga_id', 'tipo_ranking', 'url_link', 'url_editoria_ge',
                          'img_background', 'img_marca_patrocinador', 'nome')
        super(Sponsor, self).__init__(param_defaults, **kwargs)


class Status(BaseModel):
    def __init__(self, **kwargs):
        param_defaults = ('rodada_atual', 'status_mercado', 'temporada', 'times_escalados', 'fechamento',
                          'mercado_pos_rodada', 'aviso')
        super(Status, self).__init__(param_defaults, **kwargs)

    @classmethod
    def from_dict(cls, data, **kwargs):
        status_mercado = {
            1: 'Aberto',
            2: 'Fechado',
            3: 'Atualização',
            4: 'Manutenção',
            6: 'Encerrado'
        }

        data['status_mercado'] = status_mercado.get(data['status_mercado'], 'Desconhecido')
        data['fechamento'] = datetime.fromtimestamp(data['fechamento']['timestamp'])
        return super(cls, cls).from_dict(data)