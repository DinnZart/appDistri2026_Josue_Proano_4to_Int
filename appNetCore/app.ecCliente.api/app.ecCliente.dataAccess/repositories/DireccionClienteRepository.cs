using app.ecCliente.dataAccess.context;
using app.ecCliente.entities.models;

namespace app.ecCliente.dataAccess.repositories
{
    public class DireccionClienteRepository : CrudGenericService<DireccionCliente>, IDireccionClienteRepository
    {
        public DireccionClienteRepository(AppDbContext context) : base(context)
        {
        }

        public async Task Actualizar(DireccionCliente cliente)
        {
            await UpdateEntity(cliente);
        }

        public async Task Eliminar(int id)
        {
            await DeleteEntity(id);
        }

        public async Task<DireccionCliente> Insertar(DireccionCliente direcCliente)
        {
            return await InsertEntity(direcCliente);
        }

        public async Task<List<DireccionCliente>> SeleccionarTodos()
        {
            return await SelectEntitiesAll();
        }

        public async Task<DireccionCliente> SeleccionarUno(int id)
        {
            return await SelectEntity(id);
        }
    }
}
