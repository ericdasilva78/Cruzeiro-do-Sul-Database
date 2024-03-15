from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email,password,first_name,last_name,web_page,country,state,city,**extra_fields):
        """Creates and saves a User with the given information."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email),first_name=first_name,last_name=last_name,web_page=web_page,country=country,state=state,city=city,**extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,email,password,first_name,last_name,web_page,country,state,city,**extra_fields):
        """Creates and saves a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email,password,first_name,last_name,web_page,country,state,city,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """Model representing users data."""
    # User E-mail: 
    email = models.EmailField(verbose_name='email address',max_length=250,null=False,blank=False,unique=True,help_text='Enter your e-mail.')
    # User name:
    first_name = models.CharField(verbose_name='first name',max_length=100,null=False,blank=False,help_text='Enter your first name.')
    last_name = models.CharField(verbose_name='last name',max_length=100,null=False,blank=False,help_text='Enter your last name.')
    # Link to user's Web Page:
    web_page = models.URLField(verbose_name='academic web page',max_length=300,null=True,blank=True,help_text='Enter the URL of your academic web page. Ex: Google Scholar, ORCID, etc.')
    # User country:
    country = models.CharField(max_length=150,null=False,blank=False,help_text='Enter your current country.')
    # User state/province:
    state = models.CharField(max_length=150,null=False,blank=False,help_text='Enter your current state/province.')
    # User city:
    city = models.CharField(max_length=150,null=False,blank=False,help_text='Enter your current city.')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','web_page','country','state','city']

    objects = UserManager()

    def get_full_name(self):
        return f'{self.last_name}, {self.first_name}'

    def get_short_name(self):
        return f'{self.last_name}, {self.first_name}'

    def __str__(self):
        return f'{self.last_name}, {self.first_name} (Email: {self.email})'

class Facility(models.Model):
    """Model representing facilities data."""
    # Synchrotron or other X-ray facility name:
    name = models.CharField(max_length=300,null=False,blank=False,help_text='Enter the name of synchrotron or other x-ray facility.')
    # Energy of the stored current in the storage ring:
    energy = models.FloatField(null=True,blank=True,help_text='Enter the energy (in GeV) of stored current in the storage ring.')
    # Description of the x-ray source:
    xray_source = models.CharField('X-ray source',max_length=300,null=False,blank=False, help_text='Enter a description of the x-ray source. Ex: \'bend magnet\', \'undulator\', \'rotating copper anode\', etc.')
    # Facility country:
    country = models.CharField(max_length=150,null=False,blank=False,help_text='Enter the country where the facility is located.')
    # Facility state or province:
    state = models.CharField(max_length=150,null=False,blank=False,help_text='Enter the state/province where the facility is located.')
    # Facility city:
    city = models.CharField(max_length=150,null=False,blank=False,help_text='Enter the city where the facility is located.')
    # Meta class:
    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name} ({self.city}, {self.state}, {self.country})'

class Beamline(models.Model):
    """Model representing beamlines data."""
    # Beamline name:
    name = models.CharField(max_length=300,null=False,blank=False,help_text='Enter the name by which the beamline is known.')
    # How beam collimation is provided:
    collimation = models.CharField(max_length=300,null=True,blank=True,help_text='Enter a concise statement of how beam collimation is provided.')
    # How bram focusing is provided:
    focusing = models.CharField(max_length=300,null=True,blank=True,help_text='Enter a concise statement about how beam focusing is provided.')
    # How harmonic rejection is accomplished:
    harmonic_rejection = models.CharField(max_length=300,null=True,blank=True,help_text='Enter a concise statement about how harmonic rejection is accomplished.')
    # Foreign key relating to beamline's facility:
    # Cannot be deleted if some beamline is using it
    facility = models.ForeignKey(Facility,null=False,blank=False,on_delete=models.PROTECT,help_text='Choose the beamline facility.')
    # Meta class:
    class Meta:
        verbose_name = 'Beamline'
        verbose_name_plural = 'Beamlines'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name} ({self.facility.name})'
    
class Normalization(models.Model):
    """ Model representing normalized data."""
    # Name of the sample:
    name = models.CharField(max_length=300,null=False,blank=False,help_text='Enter the name of the sample.')
    # Meta class:
    class Meta:
        verbose_name = 'Normalization'
        verbose_name_plural = 'Normalizations'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'
    
class Comparison(models.Model):
    """ Model representing normalized data."""
    # Name of the sample:
    name = models.CharField(max_length=300,null=False,blank=False,help_text='Enter the name of the sample.')
    # Meta class:
    class Meta:
        verbose_name = 'Normalization'
        verbose_name_plural = 'Normalizations'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name}'

class Element(models.Model):
    """Model representing elements data."""
    ELEMENTS = (
        ('H', 'H - Hydrogen'),
        ('He','He - Helium'),
        ('Li','Li - Lithium'),
        ('Be','Be - Beryllium'),
        ('B', 'B - Boron'),
        ('C', 'C - Carbon'),
        ('N', 'N - Nitrogen'),
        ('O', 'O - Oxygen'),
        ('F', 'F - Fluorine'),
        ('Ne','Ne - Neon'),
        ('Na','Na - Sodium'),
        ('Mg','Mg - Magnesium'),
        ('Al','Al - Aluminium'),
        ('Si','Si - Silicon'),
        ('P', 'P - Phosphorus'),
        ('S', 'S - Sulfur'),
        ('Cl','Cl - Chlorine'),
        ('Ar','Ar - Argon'),
        ('K', 'K - Potassium'),
        ('Ca','Ca - Calcium'),
        ('Sc','Sc - Scandium'),
        ('Ti','Ti - Titanium'),
        ('V', 'V - Vanadium'),
        ('Cr','Cr - Chromium'),
        ('Mn','Mn - Manganese'),
        ('Fe','Fe - Iron'),
        ('Co','Co - Cobalt'),
        ('Ni','Ni - Nickel'),
        ('Cu','Cu - Copper'),
        ('Zn','Zn - Zinc'),
        ('Ga','Ga - Gallium'),
        ('Ge','Ge - Germanium'),
        ('As','As - Arsenic'),
        ('Se','Se - Selenium'),
        ('Br','Br - Bromine'),
        ('Kr','Kr - Krypton'),
        ('Rb','Rb - Rubidium'),
        ('Sr','Sr - Strontium'),
        ('Y', 'Y - Yttrium'),
        ('Zr','Zr - Zirconium'),
        ('Nb','Nb - Niobium'),
        ('Mo','Mo - Molybdenum'),
        ('Tc','Tc - Technetium'),
        ('Ru','Ru - Ruthenium'),
        ('Rh','Rh - Rhodium'),
        ('Pd','Pd - Palladium'),
        ('Ag','Ag - Silver'),
        ('Cd','Cd - Cadmium'),
        ('In','In - Indium'),
        ('Sn','Sn - Tin'),
        ('Sb','Sb - Antimony'),
        ('Te','Te - Tellurium'),
        ('I', 'I - Iodine'),
        ('Xe','Xe - Xenon'),
        ('Cs','Cs - Casium'),
        ('Ba','Ba - Barium'),
        ('La','La - Lanthanum'),
        ('Ce','Ce - Cerium'),
        ('Pr','Pr - Praseodymium'),
        ('Nd','Nd - Neodymium'),
        ('Pm','Pm - Promethium'),
        ('Sm','Sm - Samarium'),
        ('Eu','Eu - Europium'),
        ('Gd','Gd - Gadolinium'),
        ('Tb','Tb - Terbium'),
        ('Dy','Dy - Dysprosium'),
        ('Ho','Ho - Holmium'),
        ('Er','Er - Erbium'),
        ('Tm','Tm - Thulium'),
        ('Yb','Yb - Ytterbium'),
        ('Lu','Lu - Lutetium'),
        ('Hf','Hf - Hafnium'),
        ('Ta','Ta - Tantalum'),
        ('W', 'W - Tungsten'),
        ('Re','Re - Rhenium'),
        ('Os','Os - Osmium'),
        ('Ir','Ir - Iridium'),
        ('Pt','Pt - Platinum'),
        ('Au','Au - Gold'),
        ('Hg','Hg - Mercury'),
        ('TI','TI - Thallium'),
        ('Pb','Pb - Lead'),
        ('Bi','Bi - Bismuth'),
        ('Po','Po - Polonium'),
        ('At','At - Astatine'),
        ('Rn','Rn - Radon'),
        ('Fr','Fr - Francium'),
        ('Ra','Ra - Radium'),
        ('Ac','Ac - Actinium'),
        ('Th','Th - Thorium'),
        ('Pa','Pa - Protactinium'),
        ('U', 'U - Uranium'),
        ('Np','Np - Neptunium'),
        ('Pu','Pu - Plutonium'),
        ('Am','Am - Americium'),
        ('Cm','Cm - Curium'),
        ('Bk','Bk - Berkelium'),
        ('Cf','Cf - Californium'),
    )
    # Absorbing element symbol:
    symbol = models.CharField(max_length=2,choices=ELEMENTS,null=False,blank=False,help_text='Choose the absorbing element.')
    EDGES = (
        ('K','K'),
        ('L','L'),
        ('L1','L\u2081'),
        ('L2','L\u2082'),
        ('L3','L\u2083'),
        ('M','M'),
        ('M1','M\u2081'),
        ('M2','M\u2082'),
        ('M3','M\u2083'),
        ('M4','M\u2084'),
        ('M5','M\u2085'),
        ('N','N'),
        ('N1','N\u2081'),
        ('N2','N\u2082'),
        ('N3','N\u2083'),
        ('N4','N\u2084'),
        ('N5','N\u2085'),
        ('N6','N\u2086'),
        ('N7','N\u2087'),
        ('O','O'),
        ('O1','O\u2081'),
        ('O2','O\u2082'),
        ('O3','O\u2083'),
        ('O4','O\u2084'),
        ('O5','O\u2085'),
        ('P','P'),
        ('P1','P\u2081'),
        ('P2','P\u2082'),
        ('P3','P\u2083'),
    )
    ENERGIES = (
        ('H','K',13.6),
        ('He','K',24.6),
        ('Li','K',54.7),
        ('Li','L',5.3),
        ('Li','L1',5.3),
        ('Be','K',111.5),
        ('Be','L','3.0 - 8.0'),
        ('Be','L1',8.0),
        ('Be','L2',3.0),
        ('Be','L3',3.0),
        ('B','K',188.0),
        ('B','L','4.7 - 12.6'),
        ('B','L1',12.6),
        ('B','L2',4.7),
        ('B','L3',4.7),
        ('C','K',284.2),
        ('C','L','7.2 - 18.0'),
        ('C','L1',18.0),
        ('C','L2',7.2),
        ('C','L3',7.2),
        ('N','K',409.9),
        ('N','L','17.5 - 37.3'),
        ('N','L1',37.3),
        ('N','L2',17.5),
        ('N','L3',17.5),
        ('O','K',543.1),
        ('O','L','18.2 - 41.6'),
        ('O','L1',41.6),
        ('O','L2',18.2),
        ('O','L3',18.2),
        ('F','K',696.7),
        ('F','L','19.9 - 45.0'),
        ('F','L1',45.0),
        ('F','L2',19.9),
        ('F','L3',19.9),
        ('Ne','K',870.2),
        ('Ne','L','21.6 - 48.5'),
        ('Ne','L1',48.5),
        ('Ne','L2',21.7),
        ('Ne','L3',21.6),
        ('Na','K',1070.8),
        ('Na','L','30.4 - 63.5'),
        ('Na','L1',63.5),
        ('Na','L2',30.4),
        ('Na','L3',30.5),
        ('Mg','K',1303.0),
        ('Mg','L','49.21 - 88.6'),
        ('Mg','L1',88.6),
        ('Mg','L2',49.6),
        ('Mg','L3',49.21),
        ('Mg','M','1.0 - 2.0'),
        ('Mg','M1',2.0),
        ('Mg','M2',1.0),
        ('Mg','M3',1.0),
        ('Al','K',1559.0),
        ('Al','L','72.5 - 117.8'),
        ('Al','L1',117.8),
        ('Al','L2',72.9),
        ('Al','L3',72.5),
        ('Al','M','2.0 - 4.0'),
        ('Al','M1',4.0),
        ('Al','M2',2.0),
        ('Al','M3',2.0),
        ('Si','K',1839.0),
        ('Si','L','99.2 - 149.7'),
        ('Si','L1',149.7),
        ('Si','L2',99.8),
        ('Si','L3',99.2),
        ('Si','M','2.0 - 8.0'),
        ('Si','M1',8.0),
        ('Si','M2',2.0),
        ('Si','M3',2.0),
        ('P','K',2145.5),
        ('P','L','135.0 - 189.0'),
        ('P','L1',189.0),
        ('P','L2',136.0),
        ('P','L3',135.0),
        ('P','M','6.0 - 12.0'),
        ('P','M1',12.0),
        ('P','M2',7.0),
        ('P','M3',6.0),
        ('S','K',2472.0),
        ('S','L','162.5 - 230.9'),
        ('S','L1',230.9),
        ('S','L2',163.6),
        ('S','L3',162.5),
        ('S','M','7.0 - 14.0'),
        ('S','M1',14.0),
        ('S','M2',8.0),
        ('S','M3',7.0),
        ('Cl','K',2822.0),
        ('Cl','L','200.0 - 270.0'),
        ('Cl','L1',270.0),
        ('Cl','L2',202.0),
        ('Cl','L3',200.0),
        ('Cl','M','10.0 - 18.0'),
        ('Cl','M1',18.0),
        ('Cl','M2',10.0),
        ('Cl','M3',10.0),
        ('Ar','K',3205.9),
        ('Ar','L','248.4 - 326.3'),
        ('Ar','L1',326.3),
        ('Ar','L2',250.6),
        ('Ar','L3',248.4),
        ('Ar','M','15.7 - 29.3'),
        ('Ar','M1',29.3),
        ('Ar','M2',15.9),
        ('Ar','M3',15.7),
        ('K','K',3608.4),
        ('K','L','294.6 - 378.6'),
        ('K','L1',378.6),
        ('K','L2',297.3),
        ('K','L3',294.6),
        ('K','M','18.3 - 34.8'),
        ('K','M1',34.8),
        ('K','M2',18.3),
        ('K','M3',18.3),
        ('Ca','K',4038.5),
        ('Ca','L','346.2 - 438.4'),
        ('Ca','L1',438.4),
        ('Ca','L2',349.7),
        ('Ca','L3',346.2),
        ('Ca','M','25.4 - 44.3'),
        ('Ca','M1',44.3),
        ('Ca','M2',25.4),
        ('Ca','M3',25.4),
        ('Sc','K',4492.0),
        ('Sc','L','398.7 - 498.0'),
        ('Sc','L1',498.0),
        ('Sc','L2',403.6),
        ('Sc','L3',398.7),
        ('Sc','M','28.3 - 51.1'),
        ('Sc','M1',51.1),
        ('Sc','M2',28.3),
        ('Sc','M3',28.3),
        ('Ti','K',4966.0),
        ('Ti','L','453.8 - 560.9'),
        ('Ti','L1',560.9),
        ('Ti','L2',460.2),
        ('Ti','L3',453.8),
        ('Ti','M','2.0 - 58.7'),
        ('Ti','M1',58.7),
        ('Ti','M2',32.6),
        ('Ti','M3',32.6),
        ('Ti','M4',2.0),
        ('Ti','M5',2.0),
        ('V','K',5465.0),
        ('V','L','512.1 - 626.7'),
        ('V','L1',626.7),
        ('V','L2',519.8),
        ('V','L3',512.1),
        ('V','M','2.0 - 66.3'),
        ('V','M1',66.3),
        ('V','M2',37.2),
        ('V','M3',37.2),
        ('V','M4',2.0),
        ('V','M5',2.0),
        ('Cr','K',5989.0),
        ('Cr','L','574.1 - 696.0'),
        ('Cr','L1',696.0),
        ('Cr','L2',583.8),
        ('Cr','L3',574.1),
        ('Cr','M','2.0 - 74.1'),
        ('Cr','M1',74.1),
        ('Cr','M2',42.2),
        ('Cr','M3',42.2),
        ('Cr','M4',2.0),
        ('Cr','M5',2.0),
        ('Mn','K',6539.0),
        ('Mn','L','638.7 - 769.1'),
        ('Mn','L1',769.1),
        ('Mn','L2',649.9),
        ('Mn','L3',638.7),
        ('Mn','M','2.0 - 82.3'),
        ('Mn','M1',82.3),
        ('Mn','M2',47.2),
        ('Mn','M3',47.2),
        ('Mn','M4',2.0),
        ('Mn','M5',2.0),
        ('Fe','K',7112.0),
        ('Fe','L','706.8 - 844.6'),
        ('Fe','L1',844.6),
        ('Fe','L2',719.9),
        ('Fe','L3',706.8),
        ('Fe','M','2.0 - 91.3'),
        ('Fe','M1',91.3),
        ('Fe','M2',52.7),
        ('Fe','M3',52.7),
        ('Fe','M4',2.0),
        ('Fe','M5',2.0),
        ('Co','K',7709.0),
        ('Co','L','778.1 - 925.1'),
        ('Co','L1',925.1),
        ('Co','L2',793.2),
        ('Co','L3',778.1),
        ('Co','M','3.0 - 101.0'),
        ('Co','M1',101.0),
        ('Co','M2',58.9),
        ('Co','M3',59.9),
        ('Co','M4',3.0),
        ('Co','M5',3.0),
        ('Ni','K',8333.0),
        ('Ni','L','852.7 - 1008.6'),
        ('Ni','L1',1008.6),
        ('Ni','L2',870.0),
        ('Ni','L3',852.7),
        ('Ni','M','4.0 - 110.8'),
        ('Ni','M1',110.8),
        ('Ni','M2',68.0),
        ('Ni','M3',66.2),
        ('Ni','M4',4.0),
        ('Ni','M5',4.0),
        ('Cu','K',8979.0),
        ('Cu','L','932.7 - 1096.7'),
        ('Cu','L1',1096.7),
        ('Cu','L2',952.3),
        ('Cu','L3',932.7),
        ('Cu','M','5.0 - 122.5'),
        ('Cu','M1',122.5),
        ('Cu','M2',77.3),
        ('Cu','M3',75.1),
        ('Cu','M4',5.0),
        ('Cu','M5',5.0),
        ('Zn','K',9659.0),
        ('Zn','L','1021.8 - 1196.2'),
        ('Zn','L1',1196.2),
        ('Zn','L2',1044.9),
        ('Zn','L3',1021.8),
        ('Zn','M','10.1 - 139.8'),
        ('Zn','M1',139.8),
        ('Zn','M2',91.4),
        ('Zn','M3',88.6),
        ('Zn','M4',10.2),
        ('Zn','M5',10.1),
        ('Zn','N',1.0),
        ('Zn','N2',1.0),
        ('Zn','N3',1.0),
        ('Ga','K',10367.0),
        ('Ga','L','1116.4 - 1299.0'),
        ('Ga','L1',1299.0),
        ('Ga','L2',1143.2),
        ('Ga','L3',1116.4),
        ('Ga','M','18.7 - 159.51'),
        ('Ga','M1',159.51),
        ('Ga','M2',103.5),
        ('Ga','M3',100.0),
        ('Ga','M4',18.7),
        ('Ga','M5',18.7),
        ('Ga','N','1.0 - 2.0'),
        ('Ga','N1',1.0),
        ('Ga','N2',2.0),
        ('Ga','N3',2.0),
        ('Ge','K',11103.0),
        ('Ge','L','1217.0 - 1414.6'),
        ('Ge','L1',1414.6),
        ('Ge','L2',1248.1),
        ('Ge','L3',1217.0),
        ('Ge','M','29.2 - 180.1'),
        ('Ge','M1',180.1),
        ('Ge','M2',124.9),
        ('Ge','M3',120.8),
        ('Ge','M4',29.8),
        ('Ge','M5',29.2),
        ('Ge','N','3.0 - 5.0'),
        ('Ge','N1',5.0),
        ('Ge','N2',3.0),
        ('Ge','N3',3.0),
        ('As','K',11867.0),
        ('As','L','1323.6 - 1527.0'),
        ('As','L1',1527.0),
        ('As','L2',1359.1),
        ('As','L3',1323.6),
        ('As','M','41.7 - 204.7'),
        ('As','M1',204.7),
        ('As','M2',146.2),
        ('As','M3',141.2),
        ('As','M4',41.7),
        ('As','M5',41.7),
        ('As','N','3.0 - 8.0'),
        ('As','N1',8.0),
        ('As','N2',3.0),
        ('As','N3',3.0),
        ('Se','K',12658.0),
        ('Se','L','1433.9 - 1652.0'),
        ('Se','L1',1652.0),
        ('Se','L2',1474.3),
        ('Se','L3',1433.9),
        ('Se','M','54.6 - 229.6'),
        ('Se','M1',229.6),
        ('Se','M2',166.5),
        ('Se','M3',160.7),
        ('Se','M4',55.5),
        ('Se','M5',54.6),
        ('Se','N','3.0 - 12.0'),
        ('Se','N1',12.0),
        ('Se','N2',3.0),
        ('Se','N3',3.0),
        ('Br','K',13474.0),
        ('Br','L','1550.0 - 1782.0'),
        ('Br','L1',1782.0),
        ('Br','L2',1596.0),
        ('Br','L3',1550.0),
        ('Br','M','69.0 - 257.0'),
        ('Br','M1',257.0),
        ('Br','M2',189.0),
        ('Br','M3',182.0),
        ('Br','M4',70.0),
        ('Br','M5',69.0),
        ('Br','N','3.0 - 27.0'),
        ('Br','N1',27.0),
        ('Br','N2',3.0),
        ('Br','N3',3.0),
        ('Kr','K',14326.0),
        ('Kr','L','1678.4 - 1921.0'),
        ('Kr','L1',1921.0),
        ('Kr','L2',1730.9),
        ('Kr','L3',1678.4),
        ('Kr','M','93.8 - 292.8'),
        ('Kr','M1',292.8),
        ('Kr','M2',222.2),
        ('Kr','M3',214.4),
        ('Kr','M4',95.0),
        ('Kr','M5',93.8),
        ('Kr','N','14.1 - 27.5'),
        ('Kr','N1',27.5),
        ('Kr','N2',14.1),
        ('Kr','N3',14.1),
        ('Rb','K',15200.0),
        ('Rb','L','1804.0 - 2065.0'),
        ('Rb','L1',2065.0),
        ('Rb','L2',1864.0),
        ('Rb','L3',1804.0),
        ('Rb','M','112.0 - 326.7'),
        ('Rb','M1',326.7),
        ('Rb','M2',248.7),
        ('Rb','M3',239.1),
        ('Rb','M4',113.0),
        ('Rb','M5',112.0),
        ('Rb','N','15.3 - 30.5'),
        ('Rb','N1',30.5),
        ('Rb','N2',16.3),
        ('Rb','N3',15.3),
        ('Sr','K',16105.0),
        ('Sr','L','1940.0 - 2216.0'),
        ('Sr','L1',2216.0),
        ('Sr','L2',2007.0),
        ('Sr','L3',1940.0),
        ('Sr','M','134.2 - 358.7'),
        ('Sr','M1',358.7),
        ('Sr','M2',280.3),
        ('Sr','M3',270.0),
        ('Sr','M4',136.0),
        ('Sr','M5',134.2),
        ('Sr','N','20.1 - 38.9'),
        ('Sr','N1',38.9),
        ('Sr','N2',21.6),
        ('Sr','N3',20.1),
        ('Y','K',17038.0),
        ('Y','L','2080.0 - 2373.0'),
        ('Y','L1',2373.0),
        ('Y','L2',2156.0),
        ('Y','L3',2080.0),
        ('Y','M','155.8 - 392.0'),
        ('Y','M1',392.0),
        ('Y','M2',310.6),
        ('Y','M3',298.8),
        ('Y','M4',157.7),
        ('Y','M5',155.8),
        ('Y','N','23.1 - 43.8'),
        ('Y','N1',43.8),
        ('Y','N2',24.4),
        ('Y','N3',23.1),
        ('Zr','K',17998.0),
        ('Zr','L','2223.0 - 2532.0'),
        ('Zr','L1',2532.0),
        ('Zr','L2',2307.0),
        ('Zr','L3',2223.0),
        ('Zr','M','178.8 - 430.3'),
        ('Zr','M1',430.3),
        ('Zr','M2',343.5),
        ('Zr','M3',329.8),
        ('Zr','M4',181.1),
        ('Zr','M5',178.8),
        ('Zr','N','27.1 - 50.6'),
        ('Zr','N1',50.6),
        ('Zr','N2',28.5),
        ('Zr','N3',27.1),
        ('Nb','K',18986.0),
        ('Nb','L','2371.0 - 2698.0'),
        ('Nb','L1',2698.0),
        ('Nb','L2',2465.0),
        ('Nb','L3',2371.0),
        ('Nb','M','202.3 - 466.6'),
        ('Nb','M1',466.6),
        ('Nb','M2',376.1),
        ('Nb','M3',360.6),
        ('Nb','M4',205.0),
        ('Nb','M5',202.3),
        ('Nb','N','30.8 - 56.4'),
        ('Nb','N1',56.4),
        ('Nb','N2',32.6),
        ('Nb','N3',30.8),
        ('Mo','K',20000.0),
        ('Mo','L','2520.0 - 2866.0'),
        ('Mo','L1',2866.0),
        ('Mo','L2',2625.0),
        ('Mo','L3',2520.0),
        ('Mo','M','227.9 - 506.3'),
        ('Mo','M1',506.3),
        ('Mo','M2',411.6),
        ('Mo','M3',394.0),
        ('Mo','M4',231.1),
        ('Mo','M5',227.9),
        ('Mo','N','35.5 - 63.2'),
        ('Mo','N1',63.2),
        ('Mo','N2',37.6),
        ('Mo','N3',35.5),
        ('Tc','K',21044.0),
        ('Tc','L','2677.0 - 3043.0'),
        ('Tc','L1',3043.0),
        ('Tc','L2',2793.0),
        ('Tc','L3',2677.0),
        ('Tc','M','253.9 - 544.0'),
        ('Tc','M1',544.0),
        ('Tc','M2',447.6),
        ('Tc','M3',417.7),
        ('Tc','M4',257.6),
        ('Tc','M5',253.9),
        ('Tc','N','39.9 - 69.5'),
        ('Tc','N1',69.5),
        ('Tc','N2',42.3),
        ('Tc','N3',39.9),
        ('Ru','K',22117.0),
        ('Ru','L','2838.0 - 3224.0'),
        ('Ru','L1',3224.0),
        ('Ru','L2',2967.0),
        ('Ru','L3',2838.0),
        ('Ru','M','280.0 - 586.1'),
        ('Ru','M1',586.1),
        ('Ru','M2',483.3),
        ('Ru','M3',461.5),
        ('Ru','M4',284.2),
        ('Ru','M5',280.0),
        ('Ru','N','43.2 - 75.0'),
        ('Ru','N1',75.0),
        ('Ru','N2',46.3),
        ('Ru','N3',43.2),
        ('Rh','K',23220.0),
        ('Rh','L','3004.0 - 3412.0'),
        ('Rh','L1',3412.0),
        ('Rh','L2',3146.0),
        ('Rh','L3',3004.0),
        ('Rh','M','307.2 - 628.1'),
        ('Rh','M1',628.1),
        ('Rh','M2',521.3),
        ('Rh','M3',496.5),
        ('Rh','M4',311.9),
        ('Rh','M5',307.2),
        ('Rh','N','2.0 - 81.4'),
        ('Rh','N1',81.4),
        ('Rh','N2',50.5),
        ('Rh','N3',47.3),
        ('Rh','N4',2.0),
        ('Rh','N5',2.0),
        ('Pd','K',24350.0),
        ('Pd','L','3173.0 - 3604.0'),
        ('Pd','L1',3604.0),
        ('Pd','L2',3330.0),
        ('Pd','L3',3173.0),
        ('Pd','M','335.2 - 671.6'),
        ('Pd','M1',671.6),
        ('Pd','M2',559.9),
        ('Pd','M3',532.3),
        ('Pd','M4',340.5),
        ('Pd','M5',335.2),
        ('Pd','N','2.0 - 87.1'),
        ('Pd','N1',87.1),
        ('Pd','N2',55.7),
        ('Pd','N3',50.9),
        ('Pd','N4',2.0),
        ('Pd','N5',2.0),
        ('Ag','K',25514.0),
        ('Ag','L','3351.0 - 3806.0'),
        ('Ag','L1',3806.0),
        ('Ag','L2',3524.0),
        ('Ag','L3',3351.0),
        ('Ag','M','368.3 - 719.0'),
        ('Ag','M1',719.0),
        ('Ag','M2',603.8),
        ('Ag','M3',573.0),
        ('Ag','M4',374.0),
        ('Ag','M5',368.3),
        ('Ag','N','4.0 - 97.0'),
        ('Ag','N1',97.0),
        ('Ag','N2',63.7),
        ('Ag','N3',58.3),
        ('Ag','N4',4.0),
        ('Ag','N5',4.0),
        ('Cd','K',26711.0),
        ('Cd','L','3538.0 - 4018.0'),
        ('Cd','L1',4018.0),
        ('Cd','L2',3727.0),
        ('Cd','L3',3538.0),
        ('Cd','M','405.2 - 772.0'),
        ('Cd','M1',772.0),
        ('Cd','M2',652.6),
        ('Cd','M3',618.4),
        ('Cd','M4',411.9),
        ('Cd','M5',405.2),
        ('Cd','N','10.7 - 109.8'),
        ('Cd','N1',109.8),
        ('Cd','N2',63.9),
        ('Cd','N3',63.9),
        ('Cd','N4',11.7),
        ('Cd','N5',10.7),
        ('In','K',27940.0),
        ('In','L','3730.0 - 4238.0'),
        ('In','L1',4238.0),
        ('In','L2',3938.0),
        ('In','L3',3730.0),
        ('In','M','443.9 - 827.2'),
        ('In','M1',827.2),
        ('In','M2',703.2),
        ('In','M3',665.3),
        ('In','M4',451.4),
        ('In','M5',443.9),
        ('In','N','16.9 - 122.9'),
        ('In','N1',122.9),
        ('In','N2',73.5),
        ('In','N3',73.5),
        ('In','N4',17.7),
        ('In','N5',16.9),
        ('Sn','K',29200.0),
        ('Sn','L','3929.0 - 4465.0'),
        ('Sn','L1',4465.0),
        ('Sn','L2',4156.0),
        ('Sn','L3',3929.0),
        ('Sn','M','484.9 - 884.7'),
        ('Sn','M1',884.7),
        ('Sn','M2',756.5),
        ('Sn','M3',714.6),
        ('Sn','M4',493.2),
        ('Sn','M5',484.9),
        ('Sn','N','23.9 - 137.1'),
        ('Sn','N1',137.1),
        ('Sn','N2',83.6),
        ('Sn','N3',83.6),
        ('Sn','N4',24.9),
        ('Sn','N5',23.9),
        ('Sb','K',30491.0),
        ('Sb','L','4132.0 - 4698.0'),
        ('Sb','L1',4698.0),
        ('Sb','L2',4380.0),
        ('Sb','L3',4132.0),
        ('Sb','M','528.2 - 940.0'),
        ('Sb','M1',940.0),
        ('Sb','M2',812.7),
        ('Sb','M3',766.4),
        ('Sb','M4',537.5),
        ('Sb','M5',528.2),
        ('Sb','N','32.1 - 153.2'),
        ('Sb','N1',153.2),
        ('Sb','N2',95.6),
        ('Sb','N3',95.6),
        ('Sb','N4',33.3),
        ('Sb','N5',32.1),
        ('Sb','O','2.0 - 7.0'),
        ('Sb','O1',7.0),
        ('Sb','O2',2.0),
        ('Sb','O3',2.0),
        ('Te','K',31814.0),
        ('Te','L','4341.0 - 4939.0'),
        ('Te','L1',4939.0),
        ('Te','L2',4612.0),
        ('Te','L3',4341.0),
        ('Te','M','573.0 - 1006.0'),
        ('Te','M1',1006.0),
        ('Te','M2',870.8),
        ('Te','M3',820.8),
        ('Te','M4',583.4),
        ('Te','M5',573.0),
        ('Te','N','40.4 - 169.4'),
        ('Te','N1',169.4),
        ('Te','N2',103.3),
        ('Te','N3',103.3),
        ('Te','N4',41.9),
        ('Te','N5',40.4),
        ('Te','O','2.0 - 12.0'),
        ('Te','O1',12.0),
        ('Te','O2',2.0),
        ('Te','O3',2.0),
        ('I','K',33169.0),
        ('I','L','4557.0 - 5188.0'),
        ('I','L1',5188.0),
        ('I','L2',4852.0),
        ('I','L3',4557.0),
        ('I','M','619.3 - 1072.0'),
        ('I','M1',1072.0),
        ('I','M2',931.0),
        ('I','M3',875.0),
        ('I','M4',630.8),
        ('I','M5',619.3),
        ('I','N','48.9 - 186.0'),
        ('I','N1',186.0),
        ('I','N2',123.0),
        ('I','N3',123.0),
        ('I','N4',50.6),
        ('I','N5',48.9),
        ('I','O','3.0 - 14.0'),
        ('I','O1',14.0),
        ('I','O2',3.0),
        ('I','O3',3.0),
        ('Xe','K',34561.0),
        ('Xe','L','4786.0 - 5453.0'),
        ('Xe','L1',5453.0),
        ('Xe','L2',5107.0),
        ('Xe','L3',4786.0),
        ('Xe','M','676.4 - 1148.7'),
        ('Xe','M1',1148.7),
        ('Xe','M2',1002.1),
        ('Xe','M3',940.6),
        ('Xe','M4',689.0),
        ('Xe','M5',676.4),
        ('Xe','N','67.5 - 213.2'),
        ('Xe','N1',213.2),
        ('Xe','N2',146.7),
        ('Xe','N3',145.5),
        ('Xe','N4',69.5),
        ('Xe','N5',67.5),
        ('Xe','O','12.1 - 23.3'),
        ('Xe','O1',23.3),
        ('Xe','O2',13.4),
        ('Xe','O3',12.1),
        ('Cs','K',35985.0),
        ('Cs','L','5012.0 - 5714.0'),
        ('Cs','L1',5714.0),
        ('Cs','L2',5359.0),
        ('Cs','L3',5012.0),
        ('Cs','M','726.6 - 1211.0'),
        ('Cs','M1',1211.0),
        ('Cs','M2',1071.0),
        ('Cs','M3',1003.0),
        ('Cs','M4',740.5),
        ('Cs','M5',726.6),
        ('Cs','N','77.5 - 232.3'),
        ('Cs','N1',232.3),
        ('Cs','N2',172.4),
        ('Cs','N3',161.3),
        ('Cs','N4',79.8),
        ('Cs','N5',77.5),
        ('Cs','O','12.1 - 22.7'),
        ('Cs','O1',22.7),
        ('Cs','O2',14.2),
        ('Cs','O3',12.1),
        ('Ba','K',37441.0),
        ('Ba','L','5247.0 - 5989.0'),
        ('Ba','L1',5989.0),
        ('Ba','L2',5624.0),
        ('Ba','L3',5247.0),
        ('Ba','M','780.5 - 1293.0'),
        ('Ba','M1',1293.0),
        ('Ba','M2',1137.0),
        ('Ba','M3',1063.0),
        ('Ba','M4',795.7),
        ('Ba','M5',780.5),
        ('Ba','N','89.9 - 253.5'),
        ('Ba','N1',253.5),
        ('Ba','N2',192.0),
        ('Ba','N3',178.6),
        ('Ba','N4',92.6),
        ('Ba','N5',89.9),
        ('Ba','O','14.8 - 30.3'),
        ('Ba','O1',30.3),
        ('Ba','O2',17.0),
        ('Ba','O3',14.8),
        ('La','K',38925.0),
        ('La','L','5483.0 - 6266.0'),
        ('La','L1',6266.0),
        ('La','L2',5891.0),
        ('La','L3',5483.0),
        ('La','M','836.0 - 1362.0'),
        ('La','M1',1362.0),
        ('La','M2',1209.0),
        ('La','M3',1128.0),
        ('La','M4',853.0),
        ('La','M5',836.0),
        ('La','N','102.5 - 274.7'),
        ('La','N1',274.7),
        ('La','N2',205.8),
        ('La','N3',196.0),
        ('La','N4',105.3),
        ('La','N5',102.5),
        ('La','O','16.8 - 34.3'),
        ('La','O1',34.3),
        ('La','O2',19.3),
        ('La','O3',16.8),
        ('Ce','K',40443.0),
        ('Ce','L','5723.0 - 6548.0'),
        ('Ce','L1',6548.0),
        ('Ce','L2',6164.0),
        ('Ce','L3',5723.0),
        ('Ce','M','883.8 - 1436.0'),
        ('Ce','M1',1436.0),
        ('Ce','M2',1274.0),
        ('Ce','M3',1187.0),
        ('Ce','M4',902.4),
        ('Ce','M5',883.8),
        ('Ce','N','0.1 - 291.0'),
        ('Ce','N1',291.0),
        ('Ce','N2',223.2),
        ('Ce','N3',206.5),
        ('Ce','N4',109.0),
        ('Ce','N5',109.0),
        ('Ce','N6',0.1),
        ('Ce','N7',0.1),
        ('Ce','O','17.0 - 37.8'),
        ('Ce','O1',37.8),
        ('Ce','O2',19.8),
        ('Ce','O3',17.0),
        ('Pr','K',41991.0),
        ('Pr','L','5964.0 - 6835.0'),
        ('Pr','L1',6835.0),
        ('Pr','L2',6440.0),
        ('Pr','L3',5964.0),
        ('Pr','M','928.8 - 1511.0'),
        ('Pr','M1',1511.0),
        ('Pr','M2',1337.0),
        ('Pr','M3',1242.0),
        ('Pr','M4',948.3),
        ('Pr','M5',928.8),
        ('Pr','N','2.0 - 304.5'),
        ('Pr','N1',304.5),
        ('Pr','N2',236.3),
        ('Pr','N3',217.6),
        ('Pr','N4',115.1),
        ('Pr','N5',115.1),
        ('Pr','N6',2.0),
        ('Pr','N7',2.0),
        ('Pr','O','22.3 - 37.4'),
        ('Pr','O1',37.4),
        ('Pr','O2',22.3),
        ('Pr','O3',22.3),
        ('Nd','K',43569.0),
        ('Nd','L','6208.0 - 7126.0'),
        ('Nd','L1',7126.0),
        ('Nd','L2',6722.0),
        ('Nd','L3',6208.0),
        ('Nd','M','980.4 - 1575.0'),
        ('Nd','M1',1575.0),
        ('Nd','M2',1403.0),
        ('Nd','M3',1297.0),
        ('Nd','M4',1003.3),
        ('Nd','M5',980.4),
        ('Nd','N','1.5 - 319.2'),
        ('Nd','N1',319.2),
        ('Nd','N2',243.3),
        ('Nd','N3',224.6),
        ('Nd','N4',120.5),
        ('Nd','N5',120.5),
        ('Nd','N6',1.5),
        ('Nd','N7',1.5),
        ('Nd','O','21.1 - 37.5'),
        ('Nd','O1',37.5),
        ('Nd','O2',21.1),
        ('Nd','O3',21.1),
        ('Pm','K',45184.0),
        ('Pm','L','6459.0 - 7428.0'),
        ('Pm','L1',7428.0),
        ('Pm','L2',7013.0),
        ('Pm','L3',6459.0),
        ('Pm','M','1027.0 - 1650.0'),
        ('Pm','M1',1650.0),
        ('Pm','M2',1471.4),
        ('Pm','M3',1357.0),
        ('Pm','M4',1052.0),
        ('Pm','M5',1027.0),
        ('Pm','N','4.0 - 331.0'),
        ('Pm','N1',331.0),
        ('Pm','N2',242.0),
        ('Pm','N3',242.0),
        ('Pm','N4',120.0),
        ('Pm','N5',120.0),
        ('Pm','N6',4.0),
        ('Pm','N7',4.0),
        ('Pm','O','22.0 - 38.0'),
        ('Pm','O1',38.0),
        ('Pm','O2',22.0),
        ('Pm','O3',22.0),
        ('Sm','K',46834.0),
        ('Sm','L','6716.0 - 7737.0'),
        ('Sm','L1',7737.0),
        ('Sm','L2',7312.0),
        ('Sm','L3',6716.0),
        ('Sm','M','1083.4 - 1723.0'),
        ('Sm','M1',1723.0),
        ('Sm','M2',1541.0),
        ('Sm','M3',1419.8),
        ('Sm','M4',1110.9),
        ('Sm','M5',1083.4),
        ('Sm','N','5.2 - 347.2'),
        ('Sm','N1',347.2),
        ('Sm','N2',265.6),
        ('Sm','N3',247.4),
        ('Sm','N4',129.0),
        ('Sm','N5',129.0),
        ('Sm','N6',5.2),
        ('Sm','N7',5.2),
        ('Sm','O','21.3 - 37.4'),
        ('Sm','O1',37.4),
        ('Sm','O2',21.3),
        ('Sm','O3',21.3),
        ('Eu','K',48519.0),
        ('Eu','L','6977.0 - 8052.0'),
        ('Eu','L1',8052.0),
        ('Eu','L2',7617.0),
        ('Eu','L3',6977.0),
        ('Eu','M','1127.5 - 1800.0'),
        ('Eu','M1',1800.0),
        ('Eu','M2',1614.0),
        ('Eu','M3',1481.0),
        ('Eu','M4',1158.6),
        ('Eu','M5',1127.5),
        ('Eu','N','6.0 - 360.0'),
        ('Eu','N1',360.0),
        ('Eu','N2',284.0),
        ('Eu','N3',257.0),
        ('Eu','N4',133.0),
        ('Eu','N5',127.7),
        ('Eu','N6',6.0),
        ('Eu','N7',6.0),
        ('Eu','O','22.0 - 32.0'),
        ('Eu','O1',32.0),
        ('Eu','O2',22.0),
        ('Eu','O3',22.0),
        ('Gd','K',50239.0),
        ('Gd','L','7243.0 - 8376.0'),
        ('Gd','L1',8376.0),
        ('Gd','L2',7930.0),
        ('Gd','L3',7243.0),
        ('Gd','M','1189.6 - 1881.0'),
        ('Gd','M1',1881.0),
        ('Gd','M2',1688.0),
        ('Gd','M3',1544.0),
        ('Gd','M4',1221.9),
        ('Gd','M5',1189.6),
        ('Gd','N','8.6 - 378.6'),
        ('Gd','N1',378.6),
        ('Gd','N2',286.0),
        ('Gd','N3',271.0),
        ('Gd','N4',142.6),
        ('Gd','N5',142.6),
        ('Gd','N6',8.6),
        ('Gd','N7',8.6),
        ('Gd','O','20.0 - 36.0'),
        ('Gd','O1',36.0),
        ('Gd','O2',20.0),
        ('Gd','O3',20.0),
        ('Tb','K',51996.0),
        ('Tb','L','7514.0 - 8708.0'),
        ('Tb','L1',8708.0),
        ('Tb','L2',8252.0),
        ('Tb','L3',7514.0),
        ('Tb','M','1241.1 - 1968.0'),
        ('Tb','M1',1968.0),
        ('Tb','M2',1768.0),
        ('Tb','M3',1611.0),
        ('Tb','M4',1276.9),
        ('Tb','M5',1241.1),
        ('Tb','N','2.4 - 396.0'),
        ('Tb','N1',396.0),
        ('Tb','N2',322.4),
        ('Tb','N3',284.1),
        ('Tb','N4',150.5),
        ('Tb','N5',150.5),
        ('Tb','N6',7.7),
        ('Tb','N7',2.4),
        ('Tb','O','22.6 - 45.6'),
        ('Tb','O1',45.6),
        ('Tb','O2',28.7),
        ('Tb','O3',22.6),
        ('Dy','K',53789.0),
        ('Dy','L','7790.0 - 9046.0'),
        ('Dy','L1',9046.0),
        ('Dy','L2',8581.0),
        ('Dy','L3',7790.0),
        ('Dy','M','1292.0 - 2047.0'),
        ('Dy','M1',2047.0),
        ('Dy','M2',1842.0),
        ('Dy','M3',1676.0),
        ('Dy','M4',1333.0),
        ('Dy','M5',1292.0),
        ('Dy','N','4.3 - 414.2'),
        ('Dy','N1',414.2),
        ('Dy','N2',333.5),
        ('Dy','N3',293.2),
        ('Dy','N4',153.6),
        ('Dy','N5',153.6),
        ('Dy','N6',8.0),
        ('Dy','N7',4.3),
        ('Dy','O','26.3 - 49.9'),
        ('Dy','O1',49.9),
        ('Dy','O2',26.3),
        ('Dy','O3',26.3),
        ('Ho','K',55618.0),
        ('Ho','L','8071.0 - 9394.0'),
        ('Ho','L1',9394.0),
        ('Ho','L2',8918.0),
        ('Ho','L3',8071.0),
        ('Ho','M','1351.0 - 2128.0'),
        ('Ho','M1',2128.0),
        ('Ho','M2',1923.0),
        ('Ho','M3',1741.0),
        ('Ho','M4',1392.0),
        ('Ho','M5',1351.0),
        ('Ho','N','5.2 - 432.4'),
        ('Ho','N1',432.4),
        ('Ho','N2',343.5),
        ('Ho','N3',308.2),
        ('Ho','N4',160.0),
        ('Ho','N5',160.0),
        ('Ho','N6',8.6),
        ('Ho','N7',5.2),
        ('Ho','O','24.1 - 49.3'),
        ('Ho','O1',49.3),
        ('Ho','O2',30.8),
        ('Ho','O3',24.1),
        ('Er','K',57486.0),
        ('Er','L','8358.0 - 9751.0'),
        ('Er','L1',9751.0),
        ('Er','L2',9264.0),
        ('Er','L3',8358.0),
        ('Er','M','1409.0 - 2206.0'),
        ('Er','M1',2206.0),
        ('Er','M2',2006.0),
        ('Er','M3',1812.0),
        ('Er','M4',1453.0),
        ('Er','M5',1409.0),
        ('Er','N','4.7 - 449.8'),
        ('Er','N1',449.8),
        ('Er','N2',366.2),
        ('Er','N3',320.2),
        ('Er','N4',167.6),
        ('Er','N5',167.6),
        ('Er','N6',4.7),
        ('Er','N7',4.7),
        ('Er','O','24.7 - 50.6'),
        ('Er','O1',50.6),
        ('Er','O2',31.4),
        ('Er','O3',24.7),
        ('Tm','K',59390.0),
        ('Tm','L','8648.0 - 10116.0'),
        ('Tm','L1',10116.0),
        ('Tm','L2',9617.0),
        ('Tm','L3',8648.0),
        ('Tm','M','1468.0 - 2307.0'),
        ('Tm','M1',2307.0),
        ('Tm','M2',2090.0),
        ('Tm','M3',1885.0),
        ('Tm','M4',1515.0),
        ('Tm','M5',1468.0),
        ('Tm','N','4.6 - 470.9'),
        ('Tm','N1',470.9),
        ('Tm','N2',385.9),
        ('Tm','N3',332.6),
        ('Tm','N4',175.5),
        ('Tm','N5',175.5),
        ('Tm','N6',4.6),
        ('Tm','N7',4.6),
        ('Tm','O','25.0 - 54.7'),
        ('Tm','O1',54.7),
        ('Tm','O2',31.8),
        ('Tm','O3',25.0),
        ('Yb','K',61332.0),
        ('Yb','L','8944.0 - 10486.0'),
        ('Yb','L1',10486.0),
        ('Yb','L2',9978.0),
        ('Yb','L3',8944.0),
        ('Yb','M','1528.0 - 2398.0'),
        ('Yb','M1',2398.0),
        ('Yb','M2',2173.0),
        ('Yb','M3',1950.0),
        ('Yb','M4',1576.0),
        ('Yb','M5',1528.0),
        ('Yb','N','1.3 - 480.5'),
        ('Yb','N1',480.5),
        ('Yb','N2',388.7),
        ('Yb','N3',339.7),
        ('Yb','N4',191.2),
        ('Yb','N5',182.4),
        ('Yb','N6',2.5),
        ('Yb','N7',1.3),
        ('Yb','O','24.1 - 52.0'),
        ('Yb','O1',52.0),
        ('Yb','O2',30.3),
        ('Yb','O3',24.1),
        ('Lu','K',63314.0),
        ('Lu','L','9244.0 - 10870.0'),
        ('Lu','L1',10870.0),
        ('Lu','L2',10349.0),
        ('Lu','L3',9244.0),
        ('Lu','M','1589.0 - 2491.0'),
        ('Lu','M1',2491.0),
        ('Lu','M2',2264.0),
        ('Lu','M3',2024.0),
        ('Lu','M4',1639.0),
        ('Lu','M5',1589.0),
        ('Lu','N','7.5 - 506.8'),
        ('Lu','N1',506.8),
        ('Lu','N2',412.4),
        ('Lu','N3',359.2),
        ('Lu','N4',206.1),
        ('Lu','N5',196.3),
        ('Lu','N6',8.9),
        ('Lu','N7',7.5),
        ('Lu','O','26.7 - 57.3'),
        ('Lu','O1',57.3),
        ('Lu','O2',33.6),
        ('Lu','O3',26.7),
        ('Hf','K',65351.0),
        ('Hf','L','9561.0 - 11271.0'),
        ('Hf','L1',11271.0),
        ('Hf','L2',10739.0),
        ('Hf','L3',9561.0),
        ('Hf','M','1662.0 - 2601.0'),
        ('Hf','M1',2601.0),
        ('Hf','M2',2365.0),
        ('Hf','M3',2107.0),
        ('Hf','M4',1716.0),
        ('Hf','M5',1662.0),
        ('Hf','N','14.2 - 538.0'),
        ('Hf','N1',538.0),
        ('Hf','N2',438.2),
        ('Hf','N3',380.7),
        ('Hf','N4',220.0),
        ('Hf','N5',211.5),
        ('Hf','N6',15.9),
        ('Hf','N7',14.2),
        ('Hf','O','29.9 - 64.2'),
        ('Hf','O1',64.2),
        ('Hf','O2',38.0),
        ('Hf','O3',29.9),
        ('Ta','K',67416.0),
        ('Ta','L','9881.0 - 11682.0'),
        ('Ta','L1',11682.0),
        ('Ta','L2',11136.0),
        ('Ta','L3',9881.0),
        ('Ta','M','1735.0 - 2708.0'),
        ('Ta','M1',2708.0),
        ('Ta','M2',2469.0),
        ('Ta','M3',2194.0),
        ('Ta','M4',1793.0),
        ('Ta','M5',1735.0),
        ('Ta','N','21.6 - 563.4'),
        ('Ta','N1',563.4),
        ('Ta','N2',463.4),
        ('Ta','N3',400.9),
        ('Ta','N4',237.9),
        ('Ta','N5',226.4),
        ('Ta','N6',23.5),
        ('Ta','N7',21.6),
        ('Ta','O','32.7 - 69.7'),
        ('Ta','O1',69.7),
        ('Ta','O2',42.2),
        ('Ta','O3',32.7),
        ('W','K',69525.0),
        ('W','L','10207.0 - 12100.0'),
        ('W','L1',12100.0),
        ('W','L2',11544.0),
        ('W','L3',10207.0),
        ('W','M','1809.0 - 2820.0'),
        ('W','M1',2820.0),
        ('W','M2',2575.0),
        ('W','M3',2281.0),
        ('W','M4',1872.0),
        ('W','M5',1809.0),
        ('W','N','31.4 - 594.1'),
        ('W','N1',594.1),
        ('W','N2',490.4),
        ('W','N3',423.61),
        ('W','N4',255.9),
        ('W','N5',243.5),
        ('W','N6',33.6),
        ('W','N7',31.4),
        ('W','O','36.8 - 75.6'),
        ('W','O1',75.6),
        ('W','O2',45.3),
        ('W','O3',36.8),
        ('Re','K',71676.0),
        ('Re','L','10535.0 - 12527.0'),
        ('Re','L1',12527.0),
        ('Re','L2',11959.0),
        ('Re','L3',10535.0),
        ('Re','M','1883.0 - 2932.0'),
        ('Re','M1',2932.0),
        ('Re','M2',2682.0),
        ('Re','M3',2367.0),
        ('Re','M4',1949.0),
        ('Re','M5',1883.0),
        ('Re','N','40.5 - 625.4'),
        ('Re','N1',625.4),
        ('Re','N2',518.7),
        ('Re','N3',446.8),
        ('Re','N4',273.9),
        ('Re','N5',260.5),
        ('Re','N6',42.9),
        ('Re','N7',40.5),
        ('Re','O','34.6 - 83.0'),
        ('Re','O1',83.0),
        ('Re','O2',45.6),
        ('Re','O3',34.6),
        ('Os','K',73871.0),
        ('Os','L','10871.0 - 12968.0'),
        ('Os','L1',12968.0),
        ('Os','L2',12385.0),
        ('Os','L3',10871.0),
        ('Os','M','1960.0 - 3049.0'),
        ('Os','M1',3049.0),
        ('Os','M2',2792.0),
        ('Os','M3',2457.0),
        ('Os','M4',2031.0),
        ('Os','M5',1960.0),
        ('Os','N','50.7 - 658.2'),
        ('Os','N1',658.2),
        ('Os','N2',549.1),
        ('Os','N3',470.7),
        ('Os','N4',293.1),
        ('Os','N5',278.5),
        ('Os','N6',53.4),
        ('Os','N7',50.7),
        ('Os','O','44.5 - 84.0'),
        ('Os','O1',84.0),
        ('Os','O2',58.0),
        ('Os','O3',44.5),
        ('Ir','K',76111.0),
        ('Ir','L','11215.0 - 13419.0'),
        ('Ir','L1',13419.0),
        ('Ir','L2',12824.0),
        ('Ir','L3',11215.0),
        ('Ir','M','2040.0 - 3174.0'),
        ('Ir','M1',3174.0),
        ('Ir','M2',2909.0),
        ('Ir','M3',2551.0),
        ('Ir','M4',2116.0),
        ('Ir','M5',2040.0),
        ('Ir','N','60.8 - 691.1'),
        ('Ir','N1',691.1),
        ('Ir','N2',577.8),
        ('Ir','N3',495.8),
        ('Ir','N4',311.9),
        ('Ir','N5',296.3),
        ('Ir','N6',63.8),
        ('Ir','N7',60.8),
        ('Ir','O','48.0 - 95.2'),
        ('Ir','O1',95.2),
        ('Ir','O2',63.0),
        ('Ir','O3',48.0),
        ('Pt','K',78395.0),
        ('Pt','L','11564.0 - 13880.0'),
        ('Pt','L1',13880.0),
        ('Pt','L2',13273.0),
        ('Pt','L3',11564.0),
        ('Pt','M','2122.0 - 3296.0'),
        ('Pt','M1',3296.0),
        ('Pt','M2',3027.0),
        ('Pt','M3',2645.0),
        ('Pt','M4',2202.0),
        ('Pt','M5',2122.0),
        ('Pt','N','71.2 - 725.4'),
        ('Pt','N1',725.4),
        ('Pt','N2',609.1),
        ('Pt','N3',519.4),
        ('Pt','N4',331.6),
        ('Pt','N5',314.6),
        ('Pt','N6',74.5),
        ('Pt','N7',71.2),
        ('Pt','O','51.7 - 101.7'),
        ('Pt','O1',101.7),
        ('Pt','O2',65.3),
        ('Pt','O3',51.7),
        ('Au','K',80725.0),
        ('Au','L','11919.0 - 14353.0'),
        ('Au','L1',14353.0),
        ('Au','L2',13734.0),
        ('Au','L3',11919.0),
        ('Au','M','2206.0 - 3425.0'),
        ('Au','M1',3425.0),
        ('Au','M2',3148.0),
        ('Au','M3',2743.0),
        ('Au','M4',2291.0),
        ('Au','M5',2206.0),
        ('Au','N','83.9 - 762.1'),
        ('Au','N1',762.1),
        ('Au','N2',642.7),
        ('Au','N3',546.3),
        ('Au','N4',353.2),
        ('Au','N5',335.1),
        ('Au','N6',87.6),
        ('Au','N7',83.9),
        ('Au','O','5.0 - 107.2'),
        ('Au','O1',107.2),
        ('Au','O2',74.2),
        ('Au','O3',57.2),
        ('Au','O4',5.0),
        ('Au','O5',5.0),
        ('Hg','K',83102.0),
        ('Hg','L','12284.0 - 14839.0'),
        ('Hg','L1',14839.0),
        ('Hg','L2',14209.0),
        ('Hg','L3',12284.0),
        ('Hg','M','2295.0 - 3562.0'),
        ('Hg','M1',3562.0),
        ('Hg','M2',3279.0),
        ('Hg','M3',2847.0),
        ('Hg','M4',2385.0),
        ('Hg','M5',2295.0),
        ('Hg','N','99.9 - 802.2'),
        ('Hg','N1',802.2),
        ('Hg','N2',680.2),
        ('Hg','N3',576.6),
        ('Hg','N4',378.2),
        ('Hg','N5',358.8),
        ('Hg','N6',104.0),
        ('Hg','N7',99.9),
        ('Hg','O','7.8 - 127.0'),
        ('Hg','O1',127.0),
        ('Hg','O2',83.1),
        ('Hg','O3',64.5),
        ('Hg','O4',9.6),
        ('Hg','O5',7.8),
        ('Tl','K',85530.0),
        ('Tl','L','12658.0 - 15347.0'),
        ('Tl','L1',15347.0),
        ('Tl','L2',14698.0),
        ('Tl','L3',12658.0),
        ('Tl','M','2389.0 - 3704.0'),
        ('Tl','M1',3704.0),
        ('Tl','M2',3416.0),
        ('Tl','M3',2957.0),
        ('Tl','M4',2485.0),
        ('Tl','M5',2389.0),
        ('Tl','N','117.8 - 846.2'),
        ('Tl','N1',846.2),
        ('Tl','N2',720.5),
        ('Tl','N3',609.5),
        ('Tl','N4',405.7),
        ('Tl','N5',385.0),
        ('Tl','N6',122.2),
        ('Tl','N7',117.8),
        ('Tl','O','12.5 - 136.0'),
        ('Tl','O1',136.0),
        ('Tl','O2',94.6),
        ('Tl','O3',73.5),
        ('Tl','O4',14.7),
        ('Tl','O5',12.5),
        ('Pb','K',88005.0),
        ('Pb','L','13035.0 - 15861.0'),
        ('Pb','L1',15861.0),
        ('Pb','L2',15200.0),
        ('Pb','L3',13035.0),
        ('Pb','M','2484.0 - 3851.0'),
        ('Pb','M1',3851.0),
        ('Pb','M2',3554.0),
        ('Pb','M3',3066.0),
        ('Pb','M4',2586.0),
        ('Pb','M5',2484.0),
        ('Pb','N','136.9 - 891.8'),
        ('Pb','N1',891.8),
        ('Pb','N2',761.9),
        ('Pb','N3',643.5),
        ('Pb','N4',434.3),
        ('Pb','N5',412.2),
        ('Pb','N6',141.7),
        ('Pb','N7',136.9),
        ('Pb','O','18.1 - 147.0'),
        ('Pb','O1',147.0),
        ('Pb','O2',106.4),
        ('Pb','O3',83.3),
        ('Pb','O4',20.7),
        ('Pb','O5',18.1),
        ('Pb','P','1.0 - 3.0'),
        ('Pb','P1',3.0),
        ('Pb','P2',1.0),
        ('Pb','P3',1.0),
        ('Bi','K',90526.0),
        ('Bi','L','13419.0 - 16388.0'),
        ('Bi','L1',16388.0),
        ('Bi','L2',15711.0),
        ('Bi','L3',13419.0),
        ('Bi','M','2580.0 - 3999.0'),
        ('Bi','M1',3999.0),
        ('Bi','M2',3696.0),
        ('Bi','M3',3177.0),
        ('Bi','M4',2688.0),
        ('Bi','M5',2580.0),
        ('Bi','N','157.0 - 939.0'),
        ('Bi','N1',939.0),
        ('Bi','N2',805.2),
        ('Bi','N3',678.8),
        ('Bi','N4',464.0),
        ('Bi','N5',440.1),
        ('Bi','N6',162.3),
        ('Bi','N7',157.0),
        ('Bi','O','23.8 - 159.3'),
        ('Bi','O1',159.3),
        ('Bi','O2',119.0),
        ('Bi','O3',92.6),
        ('Bi','O4',26.9),
        ('Bi','O5',23.8),
        ('Bi','P','3.0 - 8.0'),
        ('Bi','P1',8.0),
        ('Bi','P2',3.0),
        ('Bi','P3',3.0),
        ('Po','K',93105.0),
        ('Po','L','13814.0 - 16939.0'),
        ('Po','L1',16939.0),
        ('Po','L2',16244.0),
        ('Po','L3',13814.0),
        ('Po','M','2683.0 - 4149.0'),
        ('Po','M1',4149.0),
        ('Po','M2',3854.0),
        ('Po','M3',3302.0),
        ('Po','M4',2798.0),
        ('Po','M5',2683.0),
        ('Po','N','184.0 - 995.0'),
        ('Po','N1',995.0),
        ('Po','N2',851.0),
        ('Po','N3',705.0),
        ('Po','N4',500.0),
        ('Po','N5',473.0),
        ('Po','N6',184.0),
        ('Po','N7',184.0),
        ('Po','O','31.0 - 177.0'),
        ('Po','O1',177.0),
        ('Po','O2',132.0),
        ('Po','O3',104.0),
        ('Po','O4',31.0),
        ('Po','O5',31.0),
        ('Po','P','1.0 - 9.0'),
        ('Po','P1',9.0),
        ('Po','P2',4.0),
        ('Po','P3',1.0),
        ('At','K',95730.0),
        ('At','L','14214.0 - 17493.0'),
        ('At','L1',17493.0),
        ('At','L2',16785.0),
        ('At','L3',14214.0),
        ('At','M','2787.0 - 4317.0'),
        ('At','M1',4317.0),
        ('At','M2',4008.0),
        ('At','M3',3426.0),
        ('At','M4',2909.0),
        ('At','M5',2787.0),
        ('At','N','210.0 - 1042.0'),
        ('At','N1',1042.0),
        ('At','N2',886.0),
        ('At','N3',740.0),
        ('At','N4',533.0),
        ('At','N5',507.0),
        ('At','N6',210.0),
        ('At','N7',210.0),
        ('At','O','40.0 - 195.0'),
        ('At','O1',195.0),
        ('At','O2',148.0),
        ('At','O3',115.0),
        ('At','O4',40.0),
        ('At','O5',40.0),
        ('At','P','1.0 - 13.0'),
        ('At','P1',13.0),
        ('At','P2',6.0),
        ('At','P3',1.0),
        ('Rn','K',98404.0),
        ('Rn','L','14619.0 - 18049.0'),
        ('Rn','L1',18049.0),
        ('Rn','L2',17337.0),
        ('Rn','L3',14619.0),
        ('Rn','M','2892.0 - 4482.0'),
        ('Rn','M1',4482.0),
        ('Rn','M2',4159.0),
        ('Rn','M3',3538.0),
        ('Rn','M4',3022.0),
        ('Rn','M5',2892.0),
        ('Rn','N','238.0 - 1097.0'),
        ('Rn','N1',1097.0),
        ('Rn','N2',929.0),
        ('Rn','N3',768.0),
        ('Rn','N4',567.0),
        ('Rn','N5',541.0),
        ('Rn','N6',238.0),
        ('Rn','N7',238.0),
        ('Rn','O','48.0 - 214.0'),
        ('Rn','O1',214.0),
        ('Rn','O2',164.0),
        ('Rn','O3',127.0),
        ('Rn','O4',48.0),
        ('Rn','O5',48.0),
        ('Rn','P','2.0 - 16.0'),
        ('Rn','P1',16.0),
        ('Rn','P2',8.0),
        ('Rn','P3',2.0),
        ('Fr','K',101137.0),
        ('Fr','L','15031.0 - 18639.0'),
        ('Fr','L1',18639.0),
        ('Fr','L2',17907.0),
        ('Fr','L3',15031.0),
        ('Fr','M','3000.0 - 4652.0'),
        ('Fr','M1',4652.0),
        ('Fr','M2',4327.0),
        ('Fr','M3',3663.0),
        ('Fr','M4',3136.0),
        ('Fr','M5',3000.0),
        ('Fr','N','268.0 - 1153.0'),
        ('Fr','N1',1153.0),
        ('Fr','N2',980.0),
        ('Fr','N3',810.0),
        ('Fr','N4',603.0),
        ('Fr','N5',577.0),
        ('Fr','N6',268.0),
        ('Fr','N7',268.0),
        ('Fr','O','58.0 - 234.0'),
        ('Fr','O1',234.0),
        ('Fr','O2',182.0),
        ('Fr','O3',140.0),
        ('Fr','O4',58.0),
        ('Fr','O5',58.0),
        ('Fr','P','7.0 - 24.0'),
        ('Fr','P1',24.0),
        ('Fr','P2',14.0),
        ('Fr','P3',7.0),
        ('Ra','K',103922.0),
        ('Ra','L','15444.0 - 19237.0'),
        ('Ra','L1',19237.0),
        ('Ra','L2',18484.0),
        ('Ra','L3',15444.0),
        ('Ra','M','3105.0 - 4822.0'),
        ('Ra','M1',4822.0),
        ('Ra','M2',4490.0),
        ('Ra','M3',3792.0),
        ('Ra','M4',3248.0),
        ('Ra','M5',3105.0),
        ('Ra','N','299.0 - 1208.0'),
        ('Ra','N1',1208.0),
        ('Ra','N2',1058.0),
        ('Ra','N3',879.0),
        ('Ra','N4',636.0),
        ('Ra','N5',603.0),
        ('Ra','N6',299.0),
        ('Ra','N7',299.0),
        ('Ra','O','68.0 - 254.0'),
        ('Ra','O1',254.0),
        ('Ra','O2',200.0),
        ('Ra','O3',153.0),
        ('Ra','O4',68.0),
        ('Ra','O5',68.0),
        ('Ra','P','12.0 - 31.0'),
        ('Ra','P1',31.0),
        ('Ra','P2',20.0),
        ('Ra','P3',12.0),
        ('Ac','K',106755.0),
        ('Ac','L','15871.0 - 19840.0'),
        ('Ac','L1',19840.0),
        ('Ac','L2',19083.0),
        ('Ac','L3',15871.0),
        ('Ac','M','3219.0 - 5002.0'),
        ('Ac','M1',5002.0),
        ('Ac','M2',4656.0),
        ('Ac','M3',3909.0),
        ('Ac','M4',3370.0),
        ('Ac','M5',3219.0),
        ('Ac','N','319.0 - 1269.0'),
        ('Ac','N1',1269.0),
        ('Ac','N2',1080.0),
        ('Ac','N3',890.0),
        ('Ac','N4',675.0),
        ('Ac','N5',639.0),
        ('Ac','N6',319.0),
        ('Ac','N7',319.0),
        ('Ac','O','80.0 - 272.0'),
        ('Ac','O1',272.0),
        ('Ac','O2',215.0),
        ('Ac','O3',167.0),
        ('Ac','O4',80.0),
        ('Ac','O5',80.0),
        ('Ac','P','15.0 - 37.0'),
        ('Ac','P1',37.0),
        ('Ac','P2',24.0),
        ('Ac','P3',15.0),
        ('Th','K',109651.0),
        ('Th','L','16300.0 - 20472.0'),
        ('Th','L1',20472.0),
        ('Th','L2',19693.0),
        ('Th','L3',16300.0),
        ('Th','M','3332.0 - 5182.0'),
        ('Th','M1',5182.0),
        ('Th','M2',4830.0),
        ('Th','M3',4046.0),
        ('Th','M4',3491.0),
        ('Th','M5',3332.0),
        ('Th','N','333.1 - 1330.0'),
        ('Th','N1',1330.0),
        ('Th','N2',1168.0),
        ('Th','N3',966.4),
        ('Th','N4',712.1),
        ('Th','N5',675.2),
        ('Th','N6',342.4),
        ('Th','N7',333.1),
        ('Th','O','85.4 - 290.0'),
        ('Th','O1',290.0),
        ('Th','O2',229.0),
        ('Th','O3',182.0),
        ('Th','O4',92.5),
        ('Th','O5',85.4),
        ('Th','P','16.6 - 41.4'),
        ('Th','P1',41.4),
        ('Th','P2',24.5),
        ('Th','P3',16.6),
        ('Pa','K',112601.0),
        ('Pa','L','16733.0 - 21105.0'),
        ('Pa','L1',21105.0),
        ('Pa','L2',20314.0),
        ('Pa','L3',16733.0),
        ('Pa','M','3442.0 - 5367.0'),
        ('Pa','M1',5367.0),
        ('Pa','M2',5001.0),
        ('Pa','M3',4174.0),
        ('Pa','M4',3611.0),
        ('Pa','M5',3442.0),
        ('Pa','N','360.0 - 1387.0'),
        ('Pa','N1',1387.0),
        ('Pa','N2',1224.0),
        ('Pa','N3',1007.0),
        ('Pa','N4',743.0),
        ('Pa','N5',708.0),
        ('Pa','N6',371.0),
        ('Pa','N7',360.0),
        ('Pa','O','94.0 - 310.0'),
        ('Pa','O1',310.0),
        ('Pa','O2',232.0),
        ('Pa','O3',187.0),
        ('Pa','O4',94.0),
        ('Pa','O5',94.0),
        ('Pa','P','17.0 - 43.0'),
        ('Pa','P1',43.0),
        ('Pa','P2',27.0),
        ('Pa','P3',17.0),
        ('U','K',115606.0),
        ('U','L','17166.0 - 21757.0'),
        ('U','L1',21757.0),
        ('U','L2',20948.0),
        ('U','L3',17166.0),
        ('U','M','3552.0 - 5548.0'),
        ('U','M1',5548.0),
        ('U','M2',5182.0),
        ('U','M3',4303.0),
        ('U','M4',3728.0),
        ('U','M5',3552.0),
        ('U','N','377.4 - 1439.0'),
        ('U','N1',1439.0),
        ('U','N2',1271.0),
        ('U','N3',1043.0),
        ('U','N4',778.3),
        ('U','N5',736.2),
        ('U','N6',388.2),
        ('U','N7',377.4),
        ('U','O','94.2 - 321.0'),
        ('U','O1',321.0),
        ('U','O2',257.0),
        ('U','O3',192.0),
        ('U','O4',102.8),
        ('U','O5',94.2),
        ('U','P','16.8 - 43.9'),
        ('U','P1',43.9),
        ('U','P2',26.8),
        ('U','P3',16.8),
        ('Np','K',118669.0),
        ('Np','L','17610.0 - 22427.0'),
        ('Np','L1',22427.0),
        ('Np','L2',21600.0),
        ('Np','L3',17610.0),
        ('Np','M','3664.0 - 5739.0'),
        ('Np','M1',5739.0),
        ('Np','M2',5366.0),
        ('Np','M3',4435.0),
        ('Np','M4',3849.0),
        ('Np','M5',3664.0),
        ('Np','N','403.0 - 1501.0'),
        ('Np','N1',1501.0),
        ('Np','N2',1328.0),
        ('Np','N3',1085.0),
        ('Np','N4',816.0),
        ('Np','N5',771.0),
        ('Np','N6',414.0),
        ('Np','N7',403.0),
        ('Np','O','101.0 - 338.0'),
        ('Np','O1',338.0),
        ('Np','O2',274.0),
        ('Np','O3',206.0),
        ('Np','O4',109.0),
        ('Np','O5',101.0),
        ('Np','P','18.0 - 47.0'),
        ('Np','P1',47.0),
        ('Np','P2',29.0),
        ('Np','P3',18.0),
        ('Pu','K',121791.0),
        ('Pu','L','18057.0 - 23104.0'),
        ('Pu','L1',23104.0),
        ('Pu','L2',22266.0),
        ('Pu','L3',18057.0),
        ('Pu','M','3775.0 - 5933.0'),
        ('Pu','M1',5933.0),
        ('Pu','M2',5547.0),
        ('Pu','M3',4563.0),
        ('Pu','M4',3970.0),
        ('Pu','M5',3775.0),
        ('Pu','N','424.0 - 1559.0'),
        ('Pu','N1',1559.0),
        ('Pu','N2',1380.0),
        ('Pu','N3',1123.0),
        ('Pu','N4',846.0),
        ('Pu','N5',798.0),
        ('Pu','N6',436.0),
        ('Pu','N7',424.0),
        ('Pu','O','102.0 - 350.0'),
        ('Pu','O1',350.0),
        ('Pu','O2',283.0),
        ('Pu','O3',213.0),
        ('Pu','O4',113.0),
        ('Pu','O5',102.0),
        ('Pu','P','16.0 - 46.0'),
        ('Pu','P1',46.0),
        ('Pu','P2',29.0),
        ('Pu','P3',16.0),
        ('Am','K',124982.0),
        ('Am','L','18510.0 - 23808.0'),
        ('Am','L1',23808.0),
        ('Am','L2',22952.0),
        ('Am','L3',18510.0),
        ('Am','M','3890.0 - 6133.0'),
        ('Am','M1',6133.0),
        ('Am','M2',5739.0),
        ('Am','M3',4698.0),
        ('Am','M4',4096.0),
        ('Am','M5',3890.0),
        ('Am','N','446.0 - 1620.0'),
        ('Am','N1',1620.0),
        ('Am','N2',1438.0),
        ('Am','N3',1165.0),
        ('Am','N4',880.0),
        ('Am','N5',829.0),
        ('Am','N6',461.0),
        ('Am','N7',446.0),
        ('Am','O','106.0 - 365.0'),
        ('Am','O1',365.0),
        ('Am','O2',298.0),
        ('Am','O3',219.0),
        ('Am','O4',116.0),
        ('Am','O5',106.0),
        ('Am','P','16.0 - 48.0'),
        ('Am','P1',48.0),
        ('Am','P2',29.0),
        ('Am','P3',16.0),
        ('Cm','K',128241.0),
        ('Cm','L','18970.0 - 24526.0'),
        ('Cm','L1',24526.0),
        ('Cm','L2',23651.0),
        ('Cm','L3',18970.0),
        ('Cm','M','4009.0 - 6337.0'),
        ('Cm','M1',6337.0),
        ('Cm','M2',5937.0),
        ('Cm','M3',4838.0),
        ('Cm','M4',4224.0),
        ('Cm','M5',4009.0),
        ('Cm','N','470.0 - 1684.0'),
        ('Cm','N1',1684.0),
        ('Cm','N2',1498.0),
        ('Cm','N3',1207.0),
        ('Cm','N4',916.0),
        ('Cm','N5',862.0),
        ('Cm','N6',484.0),
        ('Cm','N7',470.0),
        ('Cm','O','110.0 - 383.0'),
        ('Cm','O1',383.0),
        ('Cm','O2',313.0),
        ('Cm','O3',229.0),
        ('Cm','O4',124.0),
        ('Cm','O5',110.0),
        ('Cm','P','16.0 - 50.0'),
        ('Cm','P1',50.0),
        ('Cm','P2',30.0),
        ('Cm','P3',16.0),
        ('Bk','K',131556.0),
        ('Bk','L','19435.0 - 25256.0'),
        ('Bk','L1',25256.0),
        ('Bk','L2',24371.0),
        ('Bk','L3',19435.0),
        ('Bk','M','4127.0 - 6545.0'),
        ('Bk','M1',6545.0),
        ('Bk','M2',6138.0),
        ('Bk','M3',4976.0),
        ('Bk','M4',4353.0),
        ('Bk','M5',4127.0),
        ('Bk','N','495.0 - 1748.0'),
        ('Bk','N1',1748.0),
        ('Bk','N2',1558.0),
        ('Bk','N3',1249.0),
        ('Bk','N4',955.0),
        ('Bk','N5',898.0),
        ('Bk','N6',511.0),
        ('Bk','N7',495.0),
        ('Bk','O','117.0 - 399.0'),
        ('Bk','O1',399.0),
        ('Bk','O2',326.0),
        ('Bk','O3',237.0),
        ('Bk','O4',130.0),
        ('Bk','O5',117.0),
        ('Bk','P','16.0 - 52.0'),
        ('Bk','P1',52.0),
        ('Bk','P2',32.0),
        ('Bk','P3',16.0),
        ('Cf','K',134939.0),
        ('Cf','L','19907.0 - 26010.0'),
        ('Cf','L1',26010.0),
        ('Cf','L2',25108.0),
        ('Cf','L3',19907.0),
        ('Cf','M','4247.0 - 6761.0'),
        ('Cf','M1',6761.0),
        ('Cf','M2',6345.0),
        ('Cf','M3',5116.0),
        ('Cf','M4',4484.0),
        ('Cf','M5',4247.0),
        ('Cf','N','520.0 - 1813.0'),
        ('Cf','N1',1813.0),
        ('Cf','N2',1620.0),
        ('Cf','N3',1292.0),
        ('Cf','N4',991.0),
        ('Cf','N5',930.0),
        ('Cf','N6',538.0),
        ('Cf','N7',520.0),
        ('Cf','O','122.0 - 416.0'),
        ('Cf','O1',416.0),
        ('Cf','O2',341.0),
        ('Cf','O3',245.0),
        ('Cf','O4',137.0),
        ('Cf','O5',122.0),
        ('Cf','P','17.0 - 54.0'),
        ('Cf','P1',54.0),
        ('Cf','P2',33.0),
        ('Cf','P3',17.0),
    )
    # Edge of absorbing element:
    edge = models.CharField(max_length=2,choices=EDGES,blank=False,null=False,help_text='Choose the absorption edge. The generic edges L, M, N, and O should be used only for spectra spanning multiple edges.')
    # Meta class:
    class Meta:
        verbose_name = 'Element'
        verbose_name_plural = 'Elements'

    def __str__(self):
        """String for representing the Model object."""
        energy = None
        for i, tmp in enumerate(self.ENERGIES):
            if tmp[0] == self.symbol and tmp[1] == self.edge:
                energy = tmp[2]
                break
        return f'{self.symbol}: {self.edge} edge ({energy} eV)'

class Experiment(models.Model):
    """Model representing experiments."""
    
    # Experiment:
    TYPES = (
        ('1','XAS'),
        ('2','XANES'),
        ('3','EXAFS'),
        ('4','Powder diffraction'),
        ('5','XAS + Powder diffraction'),
        ('6','XANES + Powder diffraction'),
        ('7','EXAFS + Powder diffraction'),
    )
    # Experiment type:
    experiment_type = models.CharField(max_length=1,null=False,blank=False,choices=TYPES,help_text='Choose the experiment type.')
    # Title of the experiment:
    experiment_title = models.CharField(max_length=150,null=False,blank=False,help_text='Enter a title for the experiment.')
    
    # Sample:
    # Name of the sample:
    sample_name = models.CharField('Sample name',max_length=300,null=False,blank=False,help_text='Enter a text identifying the measured sample.')
    # Stoichiometry of the sample in IUPAC format:
    sample_stoichiometry_iupac = models.CharField('Stoichiometry IUPAC',max_length=300,null=False,blank=False,help_text='Enter the IUPAC stoichiometry formula of the measured sample. Ex: [Mo (C O)4 (C18 H33 P)2].')
    # Stoichiometry of the sample in moiety format:
    sample_stoichiometry_moiety = models.CharField('Stoichiometry moiety',max_length=300,null=True,blank=True,help_text='Enter the moiety stoichiometry formula of the measured sample. Ex: C40 H66 Mo O4 P2.')
    # Information about the preparation of the sample:
    sample_prep = models.CharField('Sample preparation',max_length=300,null=True,blank=True,help_text='Enter a text summarizing the method of sample preparation.')
    # Dimensions of the sample:
    sample_dimensions = models.CharField('Sample dimensions',max_length=150,null=True,blank=True,help_text='Enter the dimensions with units of the measured sample.')
    # PH of the sample:
    sample_ph = models.FloatField('Sample ph',null=True,blank=True,help_text='Enter the ph of the sample.')
    # Redox state (EH) of the sample:
    sample_eh = models.FloatField('Sample redox state (V)',null=True,blank=True,help_text='Enter the redox (oxidation-reduction) state of the measured sample.')
    # Volume of the sample:
    sample_volume = models.FloatField('Sample volume (mm\u00b3)',null=True,blank=True,help_text='Enter the volume of the measured sample.')
    # Porosity of the sample:
    sample_porosity = models.FloatField('Sample porosity (%)',null=True,blank=True,help_text='Enter the porosity of the measured sample.')
    # Densisty of the sample:
    sample_density = models.FloatField('Sample density (g/cm\u00b3)',null=True,blank=True,help_text='Enter the density of the measured sample.')
    # Concentration of the sample:
    sample_concentration = models.FloatField('Sample concentration (g/L)',null=True,blank=True,help_text='Enter the concentration of the measured sample.')
    # Resistivity of the sample:
    sample_resistivity = models.FloatField('Sample resistivity (\u03A9)',null=True,blank=True,help_text='Enter the resistivity of the measured sample.')
    # Viscosity of the sample:
    sample_viscosity = models.FloatField('Sample viscosity (Pa\u00D7s)',null=True,blank=True,help_text='Enter the viscosity of the measured sample.')
    # Electric field of the sample:
    sample_electric_field = models.FloatField('Sample electric field (V/m)',null=True,blank=True,help_text='Enter the electric field of the measured sample.')
    # Magnetic field of the sample:
    sample_magnetic_field = models.FloatField('Sample magnetic field (T)',null=True,blank=True,help_text='Enter the magnetic field of the measured sample.')
    # Magnetic moment of the sample:
    sample_magnetic_moment = models.FloatField('Sample magnetic moment (J/T)',null=True,blank=True,help_text='Enter the magnetic moment of the measured sample.')
    # Electrochemical potential of the sample:
    sample_electrochemical_potential = models.FloatField('Sample electrochemical potential (J/mol)',null=True,blank=True,help_text='Enter the electrochemical potential of the measured sample.')
    # Opacity of the sample:
    sample_opacity = models.FloatField('Sample opacity (A/mm)',null=True,blank=True,help_text='Enter the opacity of the measured sample.')
    # Purity of the sample:
    sample_purity = models.FloatField('Sample purity (%)',null=True,blank=True,help_text='Enter the purity of the measured sample.')
    # Crystal system of the sample:
    CRYSTAL_SYSTEM = (
        ('a', 'Triclinic'),
        ('b', 'Monoclinic'),
        ('c', 'Orthorhombic'),
        ('d', 'Tetragonal'),
        ('e', 'Trigonal'),
        ('f', 'Hexagonal'),
        ('g', 'Cubic'),
    )
    sample_crystal_system = models.CharField('Sample crystal system',max_length=1,null=True,blank=True,choices=CRYSTAL_SYSTEM,help_text='Enter the crystal system of the measured sample.')
    
    # Measurement conditions:
    # Temparature of the measurement:
    measurement_temperature = models.FloatField('Measurement temperature (K)',null=True,blank=True,help_text='Enter the temperature at which the sample was measured.')
    # Pressure of the measurement:
    measurement_pressure = models.FloatField('Measurement pressure (Pa)',null=True,blank=True,help_text='Enter the pressure at which the sample was measured.')
    # Current at the beginning of the scan:
    measurement_current = models.FloatField('Measurement current (mA)',null=True,blank=True,help_text='Enter the amount of stored current in the storage ring at the beginning of the scan')
    # Wavelength:
    measurement_wavelength = models.FloatField('Wavelength (nm)',null=True,blank=True,help_text='Enter the powder diffraction wavelength')
    # Diffraction radiation type:
    diffraction_radiation_type = models.CharField('Diffraction radiation type',max_length=150,null=True,blank=True,help_text='Enter the powder diffraction radiation type. Ex: synchrotron.')

    # Crystalline:
    # Space group:
    space_group = models.CharField(max_length=150,null=True,blank=True,help_text='Enter the crystalline space groupe of the sample.')
    # z:
    z = models.FloatField(null=True,blank=True,help_text='Enter the crystalline z parameter of the sample.')
    # a:
    a = models.FloatField('a (\u212B)',null=True,blank=True,help_text='Enter the crystalline a parameter of the sample.')
    # b:
    b = models.FloatField('b (\u212B)',null=True,blank=True,help_text='Enter the crystalline b parameter of the sample.')
    # c:
    c = models.FloatField('c (\u212B)',null=True,blank=True,help_text='Enter the crystalline c parameter of the sample.')
    # alpha:
    alpha = models.FloatField('alpha (°)',null=True,blank=True,help_text='Enter the crystalline alpha parameter of the sample.')
    # beta:
    beta = models.FloatField('beta (°)',null=True,blank=True,help_text='Enter the crystalline beta parameter of the sample.')
    # gama:
    gama = models.FloatField('gama (°)',null=True,blank=True,help_text='Enter the crystalline gama parameter of the sample.')

    # Powder parameters:
    # Minimum 2 theta:
    min_2_theta = models.FloatField('Min 2\u03B8',null=True,blank=True,help_text='Enter the minium 2\u03B8.')
    # Maximum 2 theta:
    max_2_theta = models.FloatField('Max 2\u03B8',null=True,blank=True,help_text='Enter the maximum 2\u03B8.')
    # Step:
    step = models.FloatField(null=True,blank=True,help_text='Enter the 2\u03B8 step.')

    # Scan:
    # Date and time of beginning of the scan:
    start_time = models.DateTimeField(null=False,blank=False,help_text='Enter the beginning time and date of the scan.')
    # Date and time of ending of the scan:
    end_time = models.DateTimeField(null=True,blank=True,help_text='Enter the ending time and date of the scan.')
    # Edge energy used in the data acquisition software:
    edge_energy = models.FloatField('Edge energy (eV)',null=True,blank=True,help_text='Enter the absorption edge used in the data acquisition software.')
    # Operational System used to acquire the data:
    os = models.CharField('Operational System',max_length=150,null=True,blank=True,help_text='Enter the operational system name (and version) used in the data acquisition.')
    # Softwares used to acquire and process the data:
    software = models.CharField(max_length=300,null=True,blank=True,help_text='Enter the softwares names (and versions) used in the data acquisition and process tasks.')

    # Monochromator:
    # Monochromator features:
    mono_name = models.CharField('Monochromator name',max_length=300,null=True,blank=True,help_text='Enter a brief text identifying the material and diffracting plane or grating spacing of the monochromator.')
    # D-spacing of monochromator under operating conditions:
    mono_d_spacing = models.FloatField('Monochromator d-spacing (\u212B)',null=True,blank=True,help_text='Enter the known d-spacing of the monochromator under operating conditions.')

    # Detector:
    # Description of incident flux:
    detector_i0 = models.CharField(max_length=300,null=True,blank=True,help_text='Enter a description of how the incident flux was measured.')
    # Description of transmission flux:
    detector_it = models.CharField(max_length=300,null=True,blank=True,help_text='Enter a description of how the transmission flux was measured.')
    # Description of fluorecence flux:
    detector_if = models.CharField(max_length=300,null=True,blank=True,help_text='Enter a description of how the fluorescence flux was measured.')

    # Relating fields:
    # Foreign key relating to the element:
    element = models.ForeignKey(Element,blank=True,null=True,on_delete=models.PROTECT,help_text='Choose the spectra\'s absorbing element and edge.')
    # Foreign key relating to the beamline:
    beamline = models.ForeignKey(Beamline,blank=False,null=False,on_delete=models.PROTECT,help_text='Choose the beamline on which the experiment was performed.')
    # Foreign key relating to the user:
    user = models.ForeignKey(User,null=True,blank=True,on_delete=models.CASCADE,help_text='Choose the user who uploaded the date.')
    
    # Spectrum data:
    # Spectrum measurement mode:
    MEASUREMENT_MODES = (
        ('t', 'Transmission'),
        ('f', 'Fluorescence'),
        ('h', 'HERFD'),
        ('r', 'Raman'),
        ('x', 'XEOL'),
        ('e', 'Electron Emission'),
    )
    spectrum_measurement_mode = models.CharField(max_length=1,null=True,blank=True,choices=MEASUREMENT_MODES,help_text='Select the measurement mode of the spectra.')
    # Spectrum data type:
    DATA_TYPES = (
        ('r','Raw data'),
        ('m','\u03BC coefficients'),
        ('n','Normalized \u03BC coefficients'),
    )
    spectrum_data_type = models.CharField(max_length=1,null=True,blank=True,choices=DATA_TYPES,help_text='Select the spectra\'s data type.')
    # File upload field for monochromator energy:
    spectrum_energy = models.FileField(null=True,blank=True,upload_to='uploads/energy/',help_text='Select the plain text file (.txt) containing the monochromator energy data. The data array must be a column vector.')
    # File upload field for the intensity of incident x-rays:
    spectrum_i0 = models.FileField(null=True,blank=True,upload_to='uploads/i0/',help_text='Select the plain text file (.txt) containing the intensity of incident x-rays (i0) data. The data array must be a column vector.')
    # File upload field for intensity of transmitted x-rays: 
    spectrum_itrans = models.FileField(null=True,blank=True,upload_to='uploads/itrans/',help_text='Select the plain text file (.txt) containing the intensity of transmitted x-rays (itrans) data. The data array must be a column vector.')
    # File upload field for intensity of fluorescence x-rays: 
    spectrum_ifluor = models.FileField(null=True,blank=True,upload_to='uploads/ifluor/',help_text='Select the plain text file (.txt) containing the intensity of fluorescence x-rays (itrans) data. The data array must be a column vector.')
    # File upload field for mu coefficients of transmitted x-rays:
    spectrum_mutrans = models.FileField(null=True,blank=True,upload_to='uploads/mutrans/',help_text='Select the plain text file (.txt) containing the \u03BC coefficients of trasmitted x-rays (\u03BCtrans) data. The data array must be a column vector.')
    # File upload field for mu coefficients of fluorescence x-rays:
    spectrum_mufluor = models.FileField(null=True,blank=True,upload_to='uploads/mufluor/',help_text='Select the plain text file (.txt) containing the \u03BC coefficients of fluorescence x-rays (\u03BCfluor) data. The data array must be a column vector.')
    # File upload field for normalized mu coefficients of transmitted x-rays:
    spectrum_normtrans = models.FileField(null=True,blank=True,upload_to='uploads/normtrans/',help_text='Select the plain text file (.txt) containing the normalized \u03BC coefficients of transmitted x-rays data. The data array must be a column vector.')
    # File upload field for normalized mu coefficients of fluorescence x-rays:
    spectrum_normfluor = models.FileField(null=True,blank=True,upload_to='uploads/normfluor/',help_text='Select the plain text file (.txt) containing the normalized \u03BC coefficients of fluorescence x-rays data. The data array must be a column vector.')
    # Description of the normalization method used:
    spectrum_norm_info = models.CharField('Normalization information',max_length=300,null=True,blank=True,help_text='Enter a description of the normalization process used.')
    # Reference spectrum:
    reference = models.BooleanField(null=True,blank=True,help_text='Select if the spectrum is a reference spectrum')

    # Diffraction data:
    # File upload field for Powder diffraction 2 theta:
    diffraction_2_theta = models.FileField('2\u03B8',null=True,blank=True,upload_to='uploads/2_theta/',help_text='Select the plain text file (.txt) containing the diffraction 2 theta data. The data array must be a column vector.')
    # File upload field for Powder diffraction intensity:
    diffraction_intensity = models.FileField(null=True,blank=True,upload_to='uploads/intensity/',help_text='Select the plain text file (.txt) containing the diffraction intensity data. The data array must be a column vector.')

    # Additional data:
    # File upload field for cif arquives:
    cif_file = models.FileField('CIF',null=True,blank=True,upload_to='uploads/cif/',help_text='Select the Crystallographic Information File (.cif) of the sample.')
    # Licence of the data:
    data_licence = models.CharField(max_length=300,null=True,blank=True,help_text='Enter the licence of the data.')

    # Additional information:
    # Upload date and time of the sample:
    upload_date = models.DateTimeField(auto_now_add=True)
    # Aditional information about the spectrum:
    additional_info = models.CharField('Additional information',max_length=300,null=True,blank=True,help_text='Enter additional information if needed')
    # doi of the document where data was published:
    doi = models.CharField(max_length=300,null=True,blank=True,help_text='Enter the doi of the document where the data was first published.')
    # Citation of the document where data was published:
    citation = models.CharField(max_length=300,null=True,blank=True,help_text='Enter the citation of the document where the data was first published.')
    
    # Meta class:
    class Meta:
        verbose_name = 'Experiment'
        verbose_name_plural = 'Experiments'

    def get_absolute_url(self):
        """Returns the URL to access a particular instance of the model."""
        return reverse('experiment-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.experiment_title

class Report(models.Model):
    """Model representing reported spectrums and diffractograms."""
    # Reported experiment:
    experiment = models.ForeignKey(Experiment,null=False,blank=False,on_delete=models.CASCADE,help_text='Choose the experiment to report.')
    # Reporter user:
    reporter = models.ForeignKey(User,null=False,blank=False,on_delete=models.CASCADE,help_text='Choose the reporter.')
    # Report motivation:
    motivation = models.CharField(max_length=300,null=False,blank=False,help_text='Enter the motivation of the report.')
    # Meta class:
    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.experiment.experiment_title}, Reporter: {self.reporter.last_name}, {self.reporter.first_name}, Reported user: {self.experiment.user.last_name}, {self.experiment.user.first_name}'
    
def normalization_function(request):
    print("re", request)
    if request.method == 'POST':
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                # Verifique o tipo de arquivo, se necessário
                if file.name.endswith('.txt') or file.name.endswith('.csv'):
                    # Lê o arquivo com pandas
                    df = pd.read_csv(file, sep=' ', header=0)

                    # Exclue as colunas vazias
                    df = df.dropna(axis=1)        

                    # Definição do intervalo da faixa inicial (restrição)

                    background = df[0:20]

                    # Tratamento dos dados usando um fit de modelo linear

                    modelo_linear = LinearModel()
                    dados_x = background.iloc[:, 0].values
                    dados_y = background.iloc[:, 1].values

                    params_linear = modelo_linear.guess(dados_y, x=dados_x)

                    resultado_fit = modelo_linear.fit(dados_y, params_linear, x=dados_x)

                    # Extrapolação para todo o intervalo do espectro

                    xwide = df.iloc[:, 0]
                    predicted_faixa_inicial = modelo_linear.eval(resultado_fit.params, x=xwide)

                    # Ajuste da faixa final XANES utilizando fit linear

                    resultados = []
                    slope_min = 1000

                    # Loop para definir o intervalo de pontos na faixa final

                    for npt in range(-20, -100, -1):
                        np_init = npt
                        np_end = -1
                        final_medida = df.iloc[np_init:np_end]
                        faixa_final = df[np_init:np_end]
                        modelo_linear = LinearModel()
                        dados_x = faixa_final.iloc[:, 0].values
                        dados_y = faixa_final.iloc[:, 1].values

                        params_linear = modelo_linear.guess(dados_y, x=dados_x)
                        resultado_fit = modelo_linear.fit(dados_y, params_linear, x=dados_x)

                        resultados.append([npt, resultado_fit.best_values['slope']])

                        # Identificação do menor valor dentro do intervalo de fit

                        if abs(resultado_fit.best_values['slope']) < slope_min:
                            slope_min = abs(resultado_fit.best_values['slope'])
                            npt_min = npt

                    # Aplicação do fit linear

                    final_medida = df.iloc[npt_min:np_end]
                    faixa_final = df[npt_min:np_end]
                    modelo_linear = LinearModel()
                    dados_x = faixa_final.iloc[:, 0].values
                    dados_y = faixa_final.iloc[:, 1].values

                    params_linear = modelo_linear.guess(dados_y, x=dados_x)
                    resultado_fit_final = modelo_linear.fit(dados_y, params_linear, x=dados_x)

                    # Extrapolação do fit no intervalo da faixa final para todo o intervalo do espectro

                    xwide = df.iloc[:, 0]
                    predicted_faixa_final = modelo_linear.eval(resultado_fit_final.params, x=xwide)

                    absorcao = df.iloc[:, 1]
                    nova_curva = absorcao - predicted_faixa_inicial

                    # Ajuste final para todos os dados de absorção do espectro

                    fit_final = absorcao/predicted_faixa_final

                    # Derivada para encontrar o ponto E0

                    x = [df.iloc[:, 0]]
                    y =  [df.iloc[:, 1]]
                    dydx = diff(y)/diff(x)

                    E0 = np.amax(dydx[0])
                    local = np.argmax(dydx[0])
                    E0x = x[0][local]

                    dydx = diff(fit_final)/diff(xwide)

                    E0 = np.amax(dydx)
                    local = np.argmax(dydx)
                    E0x = xwide[local]

                    # Interpolação para obter o ponto na extrapolação da pré-borda e pós-borda referente ao E0

                    f = interp1d(xwide, predicted_faixa_inicial)
                    ponto_borda_inicial = f(E0x)
                    g = interp1d(xwide, predicted_faixa_final)
                    ponto_borda_final = g(E0x)

                    # Normalização dos dados de absorção de raio x pela diferença do edge jump

                    edge_jump = abs(ponto_borda_final - ponto_borda_inicial)

                    absorcao_normalizada = []

                    normalizado = absorcao/edge_jump

                    absorcao_normalizada.append(normalizado)

                    pasta_destino = "C:\JupyterLab\INICIAÇÃO A PESQUISA CIENTÍFICA\Cruzeiro-do-Sul-Database\cruzeiro_do_sul_db\db_xanes"
                    os.makedirs(pasta_destino, exist_ok=True)

                    nome_arquivo = f"{file}_normalizado.txt"

                    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

                    with open(caminho_arquivo, "w") as arquivo:
                        # Escreve o cabeçalho das colunas
                        arquivo.write("Energia\tAbsorção\n")            
                        for i in range(0,len(xwide)):
                            arquivo.write(f"{xwide.iloc[i]}\t{normalizado[i]}\n")

                    df = pd.read_csv(caminho_arquivo, delimiter='\t', encoding='latin1')  # Leia o arquivo em um DataFrame pandas
                print("string", caminho_arquivo)
                return caminho_arquivo