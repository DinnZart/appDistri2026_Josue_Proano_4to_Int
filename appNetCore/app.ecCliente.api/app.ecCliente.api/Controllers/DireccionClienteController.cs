using app.ecCliente.common.DTOs;
using app.ecCliente.services.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace app.ecCliente.api.Controllers
{

    [ApiController]
    [Route("api/[controller]")]
    public class DireccionClienteController : Controller
    {
        private readonly IDireccionClienteService _direccionClienteService;

        public DireccionClienteController(IDireccionClienteService direccionClienteService)
        {

            _direccionClienteService = direccionClienteService;
        }

        // GET: api/direccioncliente
        [HttpGet("obtener-todos")]
        public async Task<IActionResult> ObtenerTodos()
        {
            var result = await _direccionClienteService.SeleccionarTodos();

            if (!result.Success)
                return StatusCode(500, result);

            return Ok(result);
        }



        // GET: api/direccioncliente/5
        [HttpGet("{id}")]
        public async Task<IActionResult> Obtener(int id)
        {
            var result = await _direccionClienteService.SeleccionarUno(id);

            if (!result.Success)
                return BadRequest(result);

            return Ok(result);
        }



        // POST: api/direccioncliente
        [HttpPost]
        public async Task<IActionResult> Crear([FromBody] DireccionClienteDTO dto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var result = await _direccionClienteService.Insertar(dto);

            if (!result.Success)
                return StatusCode(500, result);

            return Ok(result);
        }


        // PUT: api/direccioncliente/5
        [HttpPut("{id}")]
        public async Task<IActionResult> Actualizar(int id, [FromBody] DireccionClienteDTO dto)
        {
            if (!ModelState.IsValid)
                return BadRequest(ModelState);

            var result = await _direccionClienteService.Actualizar(id, dto);

            if (!result.Success)
                return StatusCode(500, result);

            return Ok(result);
        }


        // DELETE: api/direccioncliente/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> Eliminar(int id)
        {
            var result = await _direccionClienteService.Eliminar(id);

            if (!result.Success)
                return StatusCode(500, result);

            return Ok(result);
        }




    }
}
