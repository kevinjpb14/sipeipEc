# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class ActividadesProyecto(models.Model):
    idactividad = models.AutoField(db_column='idActividad', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    idproyecto = models.ForeignKey('Proyectos', models.DO_NOTHING, db_column='idProyecto', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'actividades_proyecto'


class AlineacionObjetivoOds(models.Model):
    idobjods = models.AutoField(db_column='idObjOds', primary_key=True)  # Field name made lowercase.
    idobjest = models.ForeignKey('ObjetivoEstrategico', models.DO_NOTHING, db_column='idObjEst', blank=True, null=True)  # Field name made lowercase.
    idods = models.ForeignKey('ObjetivosDesarrolloSostenible', models.DO_NOTHING, db_column='idOds', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alineacion_objetivo_ods'


class AuditDetalle(models.Model):
    idauddetalle = models.AutoField(db_column='idAudDetalle', primary_key=True)  # Field name made lowercase.
    idauditlog = models.ForeignKey('AuditLog', models.DO_NOTHING, db_column='idAuditLog', blank=True, null=True)  # Field name made lowercase.
    nombrecampo = models.CharField(db_column='nombreCampo', max_length=255, blank=True, null=True)  # Field name made lowercase.
    oldvalue = models.CharField(db_column='oldValue', max_length=255, blank=True, null=True)  # Field name made lowercase.
    newvalue = models.CharField(db_column='newValue', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'audit_detalle'


class AuditLog(models.Model):
    idauditlog = models.AutoField(db_column='idAuditLog', primary_key=True)  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='idUsuario', blank=True, null=True)  # Field name made lowercase.
    accion = models.CharField(max_length=50, blank=True, null=True)
    modulo = models.CharField(max_length=150, blank=True, null=True)
    idobjeto = models.IntegerField(db_column='idObjeto', blank=True, null=True)  # Field name made lowercase.
    strobjeto = models.CharField(db_column='strObjeto', max_length=255, blank=True, null=True)  # Field name made lowercase.
    ipaddress = models.CharField(db_column='ipAddress', max_length=50, blank=True, null=True)  # Field name made lowercase.
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    audfecha = models.DateTimeField(db_column='audFecha', blank=True, null=True)  # Field name made lowercase.
    auth_source = models.CharField(max_length=255, db_comment='Si viene de LDAP o de Django la autenticación')

    class Meta:
        managed = False
        db_table = 'audit_log'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Cantones(models.Model):
    idcanton = models.AutoField(db_column='idCanton', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    idprovincia = models.ForeignKey('Provincias', models.DO_NOTHING, db_column='idProvincia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cantones'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Indicadores(models.Model):
    idindicador = models.AutoField(db_column='idIndicador', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)
    formula = models.IntegerField(blank=True, null=True)
    unidadmedida = models.CharField(db_column='unidadMedida', max_length=255, blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indicadores'


class InstitucionSector(models.Model):
    idsector = models.AutoField(db_column='idSector', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'institucion_sector'


class InstitucionSubsector(models.Model):
    idsubsector = models.AutoField(db_column='idSubsector', primary_key=True)  # Field name made lowercase.
    idsector = models.ForeignKey(InstitucionSector, models.DO_NOTHING, db_column='idSector', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255)
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'institucion_subsector'


class Instituciones(models.Model):
    idinstitucion = models.AutoField(db_column='idInstitucion', primary_key=True)  # Field name made lowercase.
    idsector = models.IntegerField(db_column='idSector')  # Field name made lowercase.
    issubsector = models.ForeignKey(InstitucionSubsector, models.DO_NOTHING, db_column='isSubSector')  # Field name made lowercase.
    nombre = models.CharField(max_length=255)
    nivelgobierno = models.CharField(db_column='nivelGobierno', max_length=255)  # Field name made lowercase.
    estado = models.BooleanField()
    fechacreacion = models.DateTimeField(db_column='fechaCreacion')  # Field name made lowercase.
    fechaactualizacion = models.DateTimeField(db_column='fechaActualizacion', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'instituciones'


class Metas(models.Model):
    idmeta = models.AutoField(db_column='idMeta', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    tipometa = models.CharField(db_column='tipoMeta', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idindicador = models.ForeignKey(Indicadores, models.DO_NOTHING, db_column='idIndicador', blank=True, null=True)  # Field name made lowercase.
    idusuario = models.IntegerField(db_column='idUsuario', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metas'


class ObjetivoEstrategico(models.Model):
    idobjest = models.AutoField(db_column='idObjEst', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fecharegistro = models.DateTimeField(db_column='fechaRegistro')  # Field name made lowercase.
    idpnd = models.ForeignKey('PlanNacionalDesarrollo', models.DO_NOTHING, db_column='idPnd', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'objetivo_estrategico'


class ObjetivoEstrategicoHistory(models.Model):
    idobjesth = models.AutoField(db_column='idObjEstH', primary_key=True)  # Field name made lowercase.
    idobjest = models.ForeignKey(ObjetivoEstrategico, models.DO_NOTHING, db_column='idObjEst')  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fechainicio = models.DateTimeField(db_column='fechaInicio', blank=True, null=True)  # Field name made lowercase.
    fechafin = models.DateTimeField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    numversion = models.IntegerField(db_column='numVersion')  # Field name made lowercase.
    cambiadoporusr = models.IntegerField(db_column='cambiadoPorUsr', blank=True, null=True)  # Field name made lowercase.
    fechacambio = models.DateTimeField(db_column='fechaCambio')  # Field name made lowercase.
    idpnd = models.IntegerField(db_column='idPnd', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'objetivo_estrategico_history'


class ObjetivosDesarrolloSostenible(models.Model):
    idods = models.AutoField(db_column='idOds', primary_key=True)  # Field name made lowercase.
    numeroods = models.IntegerField(db_column='numeroOds', blank=True, null=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'objetivos_desarrollo_sostenible'


class Parroquias(models.Model):
    idparroquia = models.AutoField(db_column='idParroquia', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    idcanton = models.ForeignKey(Cantones, models.DO_NOTHING, db_column='idCanton', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'parroquias'


class PeriodoActividad(models.Model):
    idperiodo = models.AutoField(db_column='idPeriodo', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    valor = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    idactividad = models.ForeignKey(ActividadesProyecto, models.DO_NOTHING, db_column='idActividad', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'periodo_actividad'


class Permisos(models.Model):
    idpermiso = models.AutoField(db_column='idPermiso', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permisos'


class PlanNacionalDesarrollo(models.Model):
    idpnd = models.AutoField(db_column='idPnd', primary_key=True)  # Field name made lowercase.
    nombreeje = models.CharField(db_column='nombreEje', max_length=255)  # Field name made lowercase.
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plan_nacional_desarrollo'


class Planes(models.Model):
    idplan = models.AutoField(db_column='idPlan', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    idpnd = models.ForeignKey(PlanNacionalDesarrollo, models.DO_NOTHING, db_column='idPnd', blank=True, null=True)  # Field name made lowercase.
    nivaut = models.IntegerField(db_column='nivAut', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'planes'


class Programas(models.Model):
    idprograma = models.AutoField(db_column='idPrograma', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    idplan = models.ForeignKey(Planes, models.DO_NOTHING, db_column='idPlan', blank=True, null=True)  # Field name made lowercase.
    fechaprograma = models.DateTimeField(db_column='fechaPrograma', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'programas'


class Provincias(models.Model):
    idprovincia = models.AutoField(db_column='idProvincia', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'provincias'


class ProyectoHistory(models.Model):
    idproyectoh = models.AutoField(db_column='idProyectoH', primary_key=True)  # Field name made lowercase.
    idproyecto = models.ForeignKey('Proyectos', models.DO_NOTHING, db_column='idProyecto')  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    fechainicio = models.DateTimeField(db_column='fechaInicio', blank=True, null=True)  # Field name made lowercase.
    fechafin = models.DateTimeField(db_column='fechaFin', blank=True, null=True)  # Field name made lowercase.
    numversion = models.IntegerField(db_column='numVersion', blank=True, null=True)  # Field name made lowercase.
    cambiadoporusr = models.IntegerField(db_column='cambiadoPorUsr', blank=True, null=True)  # Field name made lowercase.
    fechacambio = models.DateTimeField(db_column='fechaCambio', blank=True, null=True)  # Field name made lowercase.
    idiambiental = models.IntegerField(db_column='idIAmbiental', blank=True, null=True)  # Field name made lowercase.
    idinstitucion = models.IntegerField(db_column='idInstitucion', blank=True, null=True)  # Field name made lowercase.
    idug = models.IntegerField(db_column='idUG', blank=True, null=True)  # Field name made lowercase.
    situacionactual = models.CharField(db_column='situacionActual', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    antecedente = models.CharField(max_length=500, blank=True, null=True)
    justificacion = models.CharField(max_length=500, blank=True, null=True)
    beneficiarios = models.CharField(max_length=255, blank=True, null=True)
    proyectosrelacionados = models.CharField(db_column='proyectosRelacionados', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idobjest = models.IntegerField(db_column='idObjEst', blank=True, null=True)  # Field name made lowercase.
    idmeta = models.IntegerField(db_column='idMeta', blank=True, null=True)  # Field name made lowercase.
    inversion = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    duracionproyecto = models.DecimalField(db_column='duracionProyecto', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    autogestion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proyecto_history'


class ProyectoImpactoAmbiental(models.Model):
    idiambiental = models.AutoField(db_column='idIAmbiental', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    descripcion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proyecto_impacto_ambiental'


class ProyectoUbiGeografica(models.Model):
    idug = models.AutoField(db_column='idUG', primary_key=True)  # Field name made lowercase.
    coordenadas = models.CharField(max_length=255, blank=True, null=True)
    idparroquia = models.ForeignKey(Parroquias, models.DO_NOTHING, db_column='idParroquia', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'proyecto_ubi_geografica'


class Proyectos(models.Model):
    idproyecto = models.AutoField(db_column='idProyecto', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=255, blank=True, null=True)
    idiambiental = models.ForeignKey(ProyectoImpactoAmbiental, models.DO_NOTHING, db_column='idIAmbiental', blank=True, null=True)  # Field name made lowercase.
    idinstitucion = models.ForeignKey(Instituciones, models.DO_NOTHING, db_column='idInstitucion', blank=True, null=True)  # Field name made lowercase.
    idug = models.ForeignKey(ProyectoUbiGeografica, models.DO_NOTHING, db_column='idUG', blank=True, null=True)  # Field name made lowercase.
    situacionactual = models.CharField(db_column='situacionActual', max_length=1000, blank=True, null=True)  # Field name made lowercase.
    antecedente = models.CharField(max_length=500, blank=True, null=True)
    justificacion = models.CharField(max_length=500, blank=True, null=True)
    beneficiarios = models.CharField(max_length=255, blank=True, null=True)
    proyectosrelacionados = models.CharField(db_column='proyectosRelacionados', max_length=255, blank=True, null=True)  # Field name made lowercase.
    idobjest = models.ForeignKey(ObjetivoEstrategico, models.DO_NOTHING, db_column='idObjEst', blank=True, null=True)  # Field name made lowercase.
    idmeta = models.ForeignKey(Metas, models.DO_NOTHING, db_column='idMeta', blank=True, null=True)  # Field name made lowercase.
    inversion = models.DecimalField(max_digits=65535, decimal_places=65535, blank=True, null=True)
    duracionproyecto = models.DecimalField(db_column='duracionProyecto', max_digits=65535, decimal_places=65535, blank=True, null=True)  # Field name made lowercase.
    autogestion = models.CharField(max_length=255, blank=True, null=True)
    idprograma = models.ForeignKey(Programas, models.DO_NOTHING, db_column='idPrograma', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'proyectos'


class Roles(models.Model):
    idrol = models.AutoField(db_column='idRol', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='idUsuario', primary_key=True)  # Field name made lowercase.
    identificacion = models.CharField(max_length=13, blank=True, null=True)
    nombres = models.CharField(max_length=100, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    mail = models.CharField(max_length=100, blank=True, null=True)
    idrol = models.ForeignKey(Roles, models.DO_NOTHING, db_column='idRol', blank=True, null=True)  # Field name made lowercase.
    idpermiso = models.ForeignKey(Permisos, models.DO_NOTHING, db_column='idPermiso', blank=True, null=True)  # Field name made lowercase.
    estado = models.BooleanField(blank=True, null=True)
    fechacreacion = models.DateTimeField(db_column='fechaCreacion', blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(max_length=255, blank=True, null=True)
    # Relación correcta con auth_user
    user = models.OneToOneField(User, on_delete=models.CASCADE, db_column='user_id', null=True)
    class Meta:
        managed = False
        db_table = 'usuario'
