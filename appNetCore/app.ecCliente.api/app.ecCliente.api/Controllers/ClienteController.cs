using app.ecCliente.common.DTOs;
using app.ecCliente.services.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace app.ecCliente.api.Controllers
{

    [ApiController]
    [Route("api/[controller]")]
    public class ClienteController : Controller
    {

        private readonly IClienteService _clienteService;

        public ClienteController(IClienteService clienteService)
        {
            _clienteService = clienteService;
        }

        [HttpGet]
        public IActionResult GetHolaMundo()
        {
            return Ok("Hola Mundo -- ClienteController");
        }


        // GET: api/cliente
        [HttpGet("obtener-todos")]
        public async Task<IActionResult> ObtenerTodos()
        {
            var result = await _clienteService.SeleccionarTodos();

            if (result.Success)
            {
                return Ok(result);
            }
            else
            {
                return StatusCode(500, result);
            }
        }

        // GET: api/cliente/5
        [HttpGet("{id}")]
        public async Task<IActionResult> Obtener(int id)
        {
            var result = await _clienteService.SeleccionarUno(id);

            if (result.Success)
            {
                return Ok(result);
            }
            else
            {
                //return NotFound(response);
                return BadRequest(result);
            }
        }


        // POST: api/cliente
        [HttpPost]
        public async Task<IActionResult> Crear([FromBody] ClienteDTO clienteDTO)
        {
            var result = await _clienteService.Insertar(clienteDTO);

            if (!result.Success)
                return StatusCode(500, result);

            return Ok(result);
        }

        // PUT: api/cliente/5
        [HttpPut("{id}")]
        public async Task<IActionResult> Actualizar(int id, [FromBody] ClienteDTO clienteDTO)
        {
            var result = await _clienteService.Actualizar(id, clienteDTO);

            if (!result.Success)
                return StatusCode(500, result);

            return Ok(result);
        }

        // DELETE: api/cliente/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> Eliminar(int id)
        {
            var result = await _clienteService.Eliminar(id);

            if (!result.Success)
                return StatusCode(500, result);

            return Ok(result);
        }
    }
}
