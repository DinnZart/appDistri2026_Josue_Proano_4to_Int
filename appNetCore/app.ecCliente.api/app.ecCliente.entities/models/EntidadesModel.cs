using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace app.ecCliente.entities.models
{
    public class EntityBase
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        public int Id { get; set; }
        public bool Estado { get; set; }
        public DateTime Fecha { get; set; }
    }

    public class Cliente : EntityBase
    {
        [Required]
        [StringLength(30)]
        public string? Nombre { get; set; }

        [Required]
        [StringLength(30)]
        public string? Apellido { get; set; }

        [Required]
        [StringLength(50)]
        public string? Email { get; set; }

        [Required]
        [StringLength(10)]
        public string? CedulaIdentidad { get; set; }

        [Required]
        public DateTime FechaNacimiento { get; set; }

        [StringLength(15)]
        public string? Telefono { get; set; }

        // Relación 1 a N
        public ICollection<DireccionCliente>? Direcciones { get; set; }
    }


    public class DireccionCliente : EntityBase
    {
        [Required]
        public int ClienteId { get; set; }

        [Required]
        [StringLength(50)]
        public string? Provincia { get; set; }

        [Required]
        [StringLength(50)]
        public string? Ciudad { get; set; }

        [Required]
        [StringLength(150)]
        public string? Direccion { get; set; }

        [StringLength(10)]
        public string? CodigoPostal { get; set; }

        // navegación
        public Cliente? Cliente { get; set; }
    }


}
