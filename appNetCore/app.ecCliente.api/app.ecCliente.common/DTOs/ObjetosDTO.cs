namespace app.ecCliente.common.DTOs
{
    public class DireccionClienteEventDto
    {
        public int ClienteId { get; set; }
        public string NombreCompleto { get; set; } = string.Empty;
        public string Email { get; set; } = string.Empty;
        public string DireccionCompleta { get; set; } = string.Empty;
    }
}
