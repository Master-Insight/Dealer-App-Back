# app/libraries/customs/base_service.py
class BaseService:
  """
  Clase base para servicios genéricos.
  Encapsula operaciones comunes sobre un DAO y manejo básico de errores.
  """

  def __init__(self, dao):
    self.dao = dao

  def list_all(self):
    """Devuelve todos los registros."""
    try:
      return self.dao.get_all()
    except Exception as e:
      raise Exception(f"[{self.__class__.__name__}] Error al listar: {e}")

  def get_by_id(self, record_id: int):
    """Devuelve un registro por su ID."""
    try:
      record = self.dao.get_by_id(record_id)
      if not record:
        raise ValueError(f"Registro con ID {record_id} no encontrado")
      return record
    except Exception as e:
      raise Exception(f"[{self.__class__.__name__}] Error al obtener ID {record_id}: {e}")

  def create(self, data: dict):
    """Crea un nuevo registro."""
    try:
      return self.dao.insert(data)
    except Exception as e:
      raise Exception(f"[{self.__class__.__name__}] Error al crear registro: {e}")

  def update(self, record_id: int, data: dict):
    """Actualiza un registro existente."""
    try:
      return self.dao.update(record_id, data)
    except Exception as e:
      raise Exception(f"[{self.__class__.__name__}] Error al actualizar ID {record_id}: {e}")

  def delete(self, record_id: int):
    """Elimina un registro existente."""
    try:
      return self.dao.delete(record_id)
    except Exception as e:
      raise Exception(f"[{self.__class__.__name__}] Error al eliminar ID {record_id}: {e}")
