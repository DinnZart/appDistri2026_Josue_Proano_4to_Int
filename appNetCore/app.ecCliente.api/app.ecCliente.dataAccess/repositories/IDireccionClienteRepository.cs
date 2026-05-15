using app.ecCliente.entities.models;

namespace app.ecCliente.dataAccess.repositories
{
    public interface IDireccionClienteRepository
    {
        Task<DireccionCliente> SeleccionarUno(int id);

        Task<DireccionCliente> Insertar(DireccionCliente cliente);

        Task<List<DireccionCliente>> SeleccionarTodos();

        Task Actualizar(DireccionCliente cliente);

        Task Eliminar(int id);
    }
}
