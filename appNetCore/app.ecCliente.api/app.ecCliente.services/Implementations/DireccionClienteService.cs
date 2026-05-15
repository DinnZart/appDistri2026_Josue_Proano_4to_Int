using app.ecCliente.common.DTOs;
using app.ecCliente.dataAccess.repositories;
using app.ecCliente.entities.models;
using app.ecCliente.services.EventMQ;
using app.ecCliente.services.Interfaces;

namespace app.ecCliente.services.Implementations
{
    public class DireccionClienteService : IDireccionClienteService
    {
        private readonly IDireccionClienteRepository _repositoryDireccionCliente;
        private readonly IClienteRepository _repositoryCliente;
        private readonly IRabbitMQService _rabbitMQService;

        public DireccionClienteService(IDireccionClienteRepository repository,
            IClienteRepository repositoryCliente,
            IRabbitMQService rabbitMQService)
        {
            _repositoryDireccionCliente = repository;
            _repositoryCliente = repositoryCliente;
            _rabbitMQService = rabbitMQService;
        }

        public async Task<BaseResponse<DireccionClienteDTO>> Insertar(DireccionClienteDTO dto)
        {
            var response = new BaseResponse<DireccionClienteDTO>();
            try
            {
                DireccionCliente entity = new()
                {
                    ClienteId = dto.ClienteId,
                    Provincia = dto.Provincia,
                    Ciudad = dto.Ciudad,
                    Direccion = dto.Direccion,
                    CodigoPostal = dto.CodigoPostal,
                    Estado = true,
                    Fecha = DateTime.Now
                };

                entity = await _repositoryDireccionCliente.Insertar(entity);

                dto.Id = entity.Id;
                response.Result = dto;
                response.Success = true;

                await EnviarMensajeClienteDireccion(entity);
            }
            catch (Exception ex)
            {
                response.Success = false;
                response.ErrorMessage = ex.Message;
            }

            return response;
        }


        public async Task<BaseResponse<DireccionClienteDTO>> SeleccionarUno(int id)
        {
            var response = new BaseResponse<DireccionClienteDTO>();

            try
            {
                var entity = await _repositoryDireccionCliente.SeleccionarUno(id);

                if (entity == null)
                {
                    response.Success = false;
                    response.ErrorMessage = "Dirección no encontrada";
                    return response;
                }

                response.Result = new DireccionClienteDTO
                {
                    Id = entity.Id,
                    ClienteId = entity.ClienteId,
                    Provincia = entity.Provincia,
                    Ciudad = entity.Ciudad,
                    Direccion = entity.Direccion,
                    CodigoPostal = entity.CodigoPostal,
                    Estado = entity.Estado
                };

                response.Success = true;
            }
            catch (Exception ex)
            {
                response.Success = false;
                response.ErrorMessage = ex.Message;
            }

            return response;
        }


        public async Task<BaseResponse<List<DireccionClienteDTO>>> SeleccionarTodos()
        {
            var response = new BaseResponse<List<DireccionClienteDTO>>();
            try
            {
                var list = await _repositoryDireccionCliente.SeleccionarTodos();

                response.Result = list.Select(d => new DireccionClienteDTO
                {
                    Id = d.Id,
                    ClienteId = d.ClienteId,
                    Provincia = d.Provincia,
                    Ciudad = d.Ciudad,
                    Direccion = d.Direccion,
                    CodigoPostal = d.CodigoPostal,
                    Estado = d.Estado
                }).ToList();

                response.Success = true;
            }
            catch (Exception ex)
            {
                response.Success = false;
                response.ErrorMessage = ex.Message;
            }
            return response;
        }

        public async Task<BaseResponse<DireccionClienteDTO>> Actualizar(int id, DireccionClienteDTO dto)
        {
            var response = new BaseResponse<DireccionClienteDTO>();
            try
            {
                DireccionCliente entity = new()
                {
                    Id = id,
                    ClienteId = dto.ClienteId,
                    Provincia = dto.Provincia,
                    Ciudad = dto.Ciudad,
                    Direccion = dto.Direccion,
                    CodigoPostal = dto.CodigoPostal,
                    Estado = true,
                    Fecha = DateTime.Now
                };

                await _repositoryDireccionCliente.Actualizar(entity);

                dto.Id = id;
                response.Result = dto;
                response.Success = true;

                await EnviarMensajeClienteDireccion(entity);
            }
            catch (Exception ex)
            {
                response.Success = false;
                response.ErrorMessage = ex.Message;
            }

            return response;
        }

        public async Task<BaseResponse<string>> Eliminar(int id)
        {
            var response = new BaseResponse<string>();

            try
            {
                await _repositoryDireccionCliente.Eliminar(id);

                response.Result = "OK";
                response.Success = true;
            }
            catch (Exception ex)
            {
                response.Success = false;
                response.ErrorMessage = ex.Message;
            }

            return response;
        }


        private async Task EnviarMensajeClienteDireccion(DireccionCliente direccion)
        {
            var cliente = await _repositoryCliente.SeleccionarUno(direccion.ClienteId);

            var direccionClienteEvent = new DireccionClienteEventDto();
            direccionClienteEvent.ClienteId = cliente.Id;
            //consultar cliente por id
            direccionClienteEvent.NombreCompleto = $"{cliente.Nombre} {cliente.Apellido}";
            direccionClienteEvent.Email = cliente.Email!;
            direccionClienteEvent.DireccionCompleta = $"{direccion.Ciudad} - {direccion.Provincia} - {direccion.Direccion} - {direccion.CodigoPostal}";
            await _rabbitMQService.PublishMessage(direccionClienteEvent, "clienteDireccionEvent");
        }
    }
}
