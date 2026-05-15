using app.ecCliente.api.EntidadEjemplo;
using Microsoft.AspNetCore.Mvc;

namespace app.ecCliente.api.Controllers
{


    [ApiController]
    [Route("api/[controller]")]
    public class PersonaController : Controller
    {
        //Lista que simula una base de datos
        private static List<Persona> personas = new List<Persona>()
        {
            new Persona { Id = 1, Nombre = "Juan", Edad = 30, Fecha = DateTime.Now, Activo = true },
            new Persona { Id = 2, Nombre = "Maria", Edad = 25, Fecha = DateTime.Now, Activo = true }
        };


        // ==============================
        // GET -> Obtener todas las personas
        // ==============================
        [HttpGet]
        public IActionResult GetPersonas()
        {
            try
            {
                //logica validacion
                return Ok(personas); //200
            }
            catch (Exception ex)
            {
                return StatusCode(500, ex.Message); //500
            }
        }


        // ==============================
        // GET -> Obtener persona por ID
        // ==============================
        [HttpGet("{idPersona}")]
        public IActionResult GetPersona(int idPersona)
        {
            try
            {
                var persona = personas.FirstOrDefault(p => p.Id == idPersona);

                if (persona == null)
                {

                    return BadRequest("Persona No encontrada"); //400
                }

                return Ok(persona); //200
            }
            catch (Exception ex)
            {
                return StatusCode(500, ex.Message); //500
            }
        }


        // ==============================
        // POST -> Crear nueva persona
        // ==============================
        [HttpPost]
        public IActionResult Post([FromBody] Persona persona)
        {
            try
            {
                if (persona == null)
                {

                    return BadRequest("Persona es requerida"); //400
                }

                persona.Id = personas.Max(p => p.Id) + 1;
                persona.Fecha = DateTime.Now;

                personas.Add(persona);

                //logica validacion
                return Ok(persona); //200
            }
            catch (Exception ex)
            {
                return StatusCode(500, ex.Message); //500
            }
        }


        // ==============================
        // PUT -> Actualizar persona
        // ==============================
        [HttpPut("{id}")]
        public IActionResult PutActualizar(int id, [FromBody] Persona persona)
        {
            try
            {
                var personaExiste = personas.FirstOrDefault(p => p.Id == id);

                if (personaExiste == null)
                {
                    return BadRequest("Persona No encontrada"); //400
                }

                personaExiste.Nombre = persona.Nombre;
                personaExiste.Edad = persona.Edad;
                personaExiste.Activo = persona.Activo;

                //logica validacion
                return Ok(personaExiste); //200
            }
            catch (Exception ex)
            {
                return StatusCode(500, ex.Message); //500
            }
        }



        // ==============================
        // DELETE -> Eliminar persona
        // ==============================
        [HttpDelete("{id}")]
        public IActionResult DeletePersona(int id)
        {
            try
            {
                var persona = personas.FirstOrDefault(p => p.Id == id);

                if (persona == null)
                {
                    return BadRequest("Persona no encontrada"); //400
                }

                personas.Remove(persona);

                return Ok("Persona elimininada correctamente"); //200
            }
            catch (Exception ex)
            {
                return StatusCode(500, ex.Message); //500
            }
        }


    }
}
