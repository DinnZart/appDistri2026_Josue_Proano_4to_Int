using app.clientesChGio.services.Implementations;
using app.ecCliente.common.EventMQ;
using app.ecCliente.dataAccess.context;
using app.ecCliente.dataAccess.repositories;
using app.ecCliente.services.EventMQ;
using app.ecCliente.services.Implementations;
using app.ecCliente.services.Interfaces;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();


//LA CADENA DE CONEXION ESTA EN EL appsettings.json
//CON EL SIGUIENTA LINEA OBTENEMOS LA CADENA DE CONEXION A SQL SERVER
var conSqlServer = builder.Configuration.GetConnectionString("BDDSqlServer")!;
builder.Services.AddDbContext<AppDbContext>(options =>
{
    options.UseSqlServer(conSqlServer);
    options.LogTo(Console.WriteLine, LogLevel.Information).EnableSensitiveDataLogging();
});

// Leer la configuración de RabbitMQ desde el appsettings.json y lo setea en la clase RabbitMQSettings
builder.Services.Configure<RabbitMQSettings>(builder.Configuration.GetSection("rabbitmq"));

//declarar servicio y repositorios
builder.Services.AddScoped<IClienteRepository, ClienteRepository>();
builder.Services.AddScoped<IClienteService, ClienteService>();

builder.Services.AddScoped<IDireccionClienteRepository, DireccionClienteRepository>();
builder.Services.AddScoped<IDireccionClienteService, DireccionClienteService>();

builder.Services.AddSingleton<IRabbitMQService, RabbitMQService>();

var app = builder.Build();

// ========================================================================
// BLOQUE AÑADIDO: APLICAR MIGRACIONES AUTOMÁTICAMENTE AL INICIAR
// ========================================================================
using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    try
    {
        var context = services.GetRequiredService<AppDbContext>();
        // Ejecuta las migraciones pendientes. Si la base de datos no existe, la crea.
        context.Database.Migrate();
    }
    catch (Exception ex)
    {
        var logger = services.GetRequiredService<ILogger<Program>>();
        logger.LogError(ex, "Un error ocurrió durante la migración de la base de datos.");
    }
}
// ========================================================================

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();

app.UseAuthorization();

app.MapControllers();

app.Run();
