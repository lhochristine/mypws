REPO_CHOICES = (
    ("core2", "core2"),
    ("ops2", "ops2"),
    ("pws2", 'pws2'),
    ("test2", 'test2')
)

MODULE_CHOICES = (
    ('core2', (
        ('JCore', 'JCore'),
        ('JCore/BL_Common', 'JCore/BL_Common'),
        ('JCore/BL', 'JCore/BL'),
        ('JCore/Common', 'JCore/Common'),
    )),
    ('ops2', (
        ('Ops', 'Ops'),
        ('DevOps/Build', 'DevOps/Build'),
        ('DevOps/Deploy', 'DevOps/Deploy'),
    )),
    ('pws2', (
        ('PWS', 'PWS'),
    )),
    ('test2', (
        ('Scripts', 'Scripts'),
        ('Tools', 'Tools'),
    )),
)

GROUP_CHOICES = (
    ("svnadmin", "svnadmin"),
    ("buildadmin", "buildadmin"),
    ("CMIP_rw", "CMIP_rw"),
    ("CMIP_ro", "CMIP_ro"),
    ("GatewayBE_rw", "GatewayBE_rw"),
    ("GatewayBE_ro", "GatewayBE_ro"),
    ("BL_rw", "BW_rw"),
    ("BL_ro", "BL_ro"),
)

PERM_CHOICES = (
    ("r", "ReadOnly"),
    ("rw", "ReadWrite"),
)