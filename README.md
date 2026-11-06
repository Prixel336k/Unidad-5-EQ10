# FarmaExpress - Sistema de Gestión y Automatización de Lógica de Negocio

Este repositorio contiene la implementación y la suite de pruebas automatizadas para **FarmaExpress**, desarrollada como parte del Proyecto Integrador de Aprendizaje (PIA) de la Unidad 5 de Componentes de Lógica de Negocio.

---

## 1. Requisitos Previos e Instalación

Para configurar el entorno de desarrollo y ejecutar el proyecto localmente, siga los siguientes pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Prixel336k/Unidad-5-EQ10.git](https://github.com/Prixel336k/Unidad-5-EQ10.git)
   cd Unidad-5-EQ10

Crear y activar el entorno virtual:

En Windows (PowerShell):

PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
En Linux / macOS:

Bash
python3 -m venv .venv
source .venv/bin/activate

2. Instalar las dependencias del proyecto:

Bash
python -m pip install -r requirements.txt

3. Explicación de la Arquitectura
El sistema está diseñado bajo los principios de Domain-Driven Design (DDD) y arquitectura hexagonal, separando claramente las reglas del negocio de los detalles de infraestructura:

Capa de Dominio (src/domain/): Contiene las entidades, agregados y objetos de valor (como InventarioDeProducto, Lote, Venta y ReglaDeVendibilidad). Las reglas críticas (como control de stock FEFO, bloqueo de productos caducados y validación de recetas) residen estrictamente aquí, aisladas de bases de datos o frameworks externos.

Capa de Aplicación (src/application/): Orquesta los casos de uso a través de servicios de aplicación aplicando un enfoque CQRS básico (comandos que modifican estado y consultas que retornan DTOs de lectura).

Capa de Infraestructura (src/repository/): Gestiona la persistencia mediante SQLAlchemy y SQLite, implementando el patrón Unit of Work para garantizar atomicidad (commit/rollback) ante transacciones o fallos externos (como pasarelas de pago simuladas mediante Mocks).

Integración Continua (CI/CD): Configurado mediante GitHub Actions (.github/workflows/ci.yml) para ejecutar automáticamente el linter de Ruff y las pruebas con cobertura en cada push o pull request.
