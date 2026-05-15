using app.ecCliente.entities.models;
using Microsoft.EntityFrameworkCore;

namespace app.ecCliente.dataAccess.context
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {

        }

        public DbSet<Cliente> Clientes { get; set; }
        public DbSet<DireccionCliente> DireccionClientes { get; set; }
    }
}
