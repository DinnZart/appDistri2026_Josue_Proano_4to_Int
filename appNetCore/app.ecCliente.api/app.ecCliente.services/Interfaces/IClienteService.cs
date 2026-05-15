using app.ecCliente.common.DTOs;

namespace app.ecCliente.services.Interfaces
{
    public interface IClienteService
    {
        Task<BaseResponse<ClienteDTO>> Insertar(ClienteDTO clienteDTO);


        Task<BaseResponse<ClienteDTO>> SeleccionarUno(int id);


        Task<BaseResponse<List<ClienteDTO>>> SeleccionarTodos();

        Task<BaseResponse<ClienteDTO>> Actualizar(int id, ClienteDTO cliente);

        Task<BaseResponse<string>> Eliminar(int id);


    }
}
