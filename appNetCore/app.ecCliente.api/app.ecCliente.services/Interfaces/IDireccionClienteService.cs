using app.ecCliente.common.DTOs;

namespace app.ecCliente.services.Interfaces
{
    public interface IDireccionClienteService
    {
        Task<BaseResponse<DireccionClienteDTO>> Insertar(DireccionClienteDTO clienteDTO);


        Task<BaseResponse<DireccionClienteDTO>> SeleccionarUno(int id);


        Task<BaseResponse<List<DireccionClienteDTO>>> SeleccionarTodos();

        Task<BaseResponse<DireccionClienteDTO>> Actualizar(int id, DireccionClienteDTO cliente);

        Task<BaseResponse<string>> Eliminar(int id);
    }
}
