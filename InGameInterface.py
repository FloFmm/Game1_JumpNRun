import pygame
import copy
class InGameInterface:
    def __init__(self, player, current_window_width,  current_window_height):
        self.old_window_width = current_window_width
        self.old_window_height = current_window_height
        self.player= player

        self.import_images()
        self.scale_to_window_size(current_window_width, current_window_height)


    def import_images(self):
        self.health_bar_image = pygame.image.load("images/interface/health_bar.png")
        self.health_bar_image_inner = pygame.image.load("images/interface/health_bar_inner.png")
        self.health_bar_image.convert()
        self.health_bar_image_inner.convert()
        self.health_bar_image_to_draw = copy.copy(self.health_bar_image).convert()
        self.health_bar_image_inner_to_draw = copy.copy(self.health_bar_image_inner).convert()

        self.stamina_bar_image = pygame.image.load("images/interface/health_bar.png")
        self.stamina_bar_image.convert()
        self.stamina_bar_image_to_draw = copy.copy(self.stamina_bar_image).convert()

        self.mana_bar_image = pygame.image.load("images/interface/health_bar.png")
        self.mana_bar_image.convert()
        self.mana_bar_image_to_draw = copy.copy(self.mana_bar_image).convert()

    def scale_to_window_size(self, new_window_width, new_window_height):
        #set design stuff
        self.distance_between_bars = new_window_height / 30
        self.distance_from_edge = new_window_width / 100
        self.bar_height = int(new_window_height/14)
        self.bar_width = int(new_window_width/7)

        #set bar position
        self.health_bar_position = (self.distance_from_edge, self.distance_from_edge)
        self.stamina_bar_position = (self.distance_from_edge, self.distance_from_edge +
                                          self.distance_between_bars + self.bar_height)
        self.mana_bar_position = (self.distance_from_edge, self.distance_from_edge +
                                          self.distance_between_bars*2 + self.bar_height*2)

        #scale images
        self.health_bar_image_to_draw = copy.copy(self.health_bar_image).convert_alpha()
        self.health_bar_image_to_draw = pygame.transform.scale(self.health_bar_image_to_draw,
                                                               (self.bar_width, self.bar_height))
        self.health_bar_image_inner_to_draw = copy.copy(self.health_bar_image_inner).convert_alpha()
        self.health_bar_image_inner_to_draw = pygame.transform.scale(self.health_bar_image_inner_to_draw,
                                                               (self.bar_width, self.bar_height))

        self.stamina_bar_image_to_draw = copy.copy(self.stamina_bar_image).convert_alpha()
        self.stamina_bar_image_to_draw = pygame.transform.scale(self.stamina_bar_image_to_draw,
                                                                (self.bar_width, self.bar_height))

        self.mana_bar_image_to_draw = copy.copy(self.mana_bar_image).convert_alpha()
        self.mana_bar_image_to_draw = pygame.transform.scale(self.mana_bar_image_to_draw,
                                                             (self.bar_width, self.bar_height))

        #number properties
        self.fontSize = int(self.bar_height*3/4)
        self.font = pygame.font.SysFont('centuryschoolbook', self.fontSize)
        self.font.set_bold(True)
        '''['arial', 'arialblack', 'bahnschrift', 'calibri', 'cambriacambriamath', 'cambria', 'candara', 'comicsansms',
         'consolas', 'constantia', 'corbel', 'couriernew', 'ebrima', 'franklingothicmedium', 'gabriola', 'gadugi',
         'georgia', 'impact', 'inkfree', 'javanesetext', 'leelawadeeui', 'leelawadeeuisemilight', 'lucidaconsole',
         'lucidasans', 'malgungothic', 'malgungothicsemilight', 'microsofthimalaya',
         'microsoftjhengheimicrosoftjhengheiui', 'microsoftjhengheimicrosoftjhengheiuibold',
         'microsoftjhengheimicrosoftjhengheiuilight', 'microsoftnewtailue', 'microsoftphagspa', 'microsoftsansserif',
         'microsofttaile', 'microsoftyaheimicrosoftyaheiui', 'microsoftyaheimicrosoftyaheiuibold',
         'microsoftyaheimicrosoftyaheiuilight', 'microsoftyibaiti', 'mingliuextbpmingliuextbmingliuhkscsextb',
         'mongolianbaiti', 'msgothicmsuigothicmspgothic', 'mvboli', 'myanmartext', 'nirmalaui', 'nirmalauisemilight',
         'palatinolinotype', 'segoefluenticons', 'segoemdl2assets', 'segoeprint', 'segoescript', 'segoeui',
         'segoeuiblack', 'segoeuiemoji', 'segoeuihistoric', 'segoeuisemibold', 'segoeuisemilight', 'segoeuisymbol',
         'segoeuivariable', 'simsunnsimsun', 'simsunextb', 'sitkatext', 'sylfaen', 'symbol', 'tahoma', 'timesnewroman',
         'trebuchetms', 'verdana', 'webdings', 'wingdings', 'yugothicyugothicuisemiboldyugothicuibold',
         'yugothicyugothicuilight', 'yugothicmediumyugothicuiregular', 'yugothicregularyugothicuisemilight',
         'holomdl2assets', 'arialnova', 'arialnovacond', 'georgiapro', 'georgiaproblack', 'georgiaprocond',
         'georgiaprocondblack', 'georgiaprocondsemibold', 'georgiaprosemibold', 'gillsansnova', 'gillsansnovacond',
         'gillsansnovacondlt', 'gillsansnovacondultra', 'gillsansnovacondxbd', 'gillsansnovalt', 'gillsansnovaultra',
         'neuehaasgrotesktextpro', 'rockwellnova', 'rockwellnovacond', 'rockwellnovaextra', 'verdanapro',
         'verdanaproblack', 'verdanaprocond', 'verdanaprocondblack', 'verdanaprocondsemibold', 'verdanaprosemibold',
         'neuehaasgrotesktextpromedium', 'agencyfbfett', 'agencyfb', 'algerian', 'bookantiquafett',
         'bookantiquafettkursiv', 'bookantiquakursiv', 'arialfett', 'arialfettkursiv', 'arialkursiv', 'arialrounded',
         'baskervilleoldface', 'bauhaus93', 'bell', 'bellfett', 'bellkursiv', 'bernardcondensed', 'bookantiqua',
         'bodonifett', 'bodonifettkursiv', 'bodoniblackkursiv', 'bodoniblack', 'bodonicondensedfett',
         'bodonicondensedfettkursiv', 'bodonicondensedkursiv', 'bodonicondensed', 'bodonikursiv',
         'bodonipostercompressed', 'bodoni', 'bookmanoldstyle', 'bookmanoldstylefett', 'bookmanoldstylefettkursiv',
         'bookmanoldstylekursiv', 'bradleyhanditc', 'britannic', 'berlinsansfbfett', 'berlinsansfbdemifett',
         'berlinsansfb', 'broadway', 'brushscriptkursiv', 'bookshelfsymbol7', 'californianfbfett',
         'californianfbkursiv', 'californianfb', 'calisto', 'calistofett', 'calistofettkursiv', 'calistokursiv',
         'castellar', 'centuryschoolbook', 'centaur', 'century', 'chiller', 'colonna', 'cooperblack',
         'copperplategothic', 'curlz', 'dubai', 'dubaimedium', 'dubairegular', 'elephant', 'elephantkursiv',
         'engravers', 'erasitc', 'erasdemiitc', 'erasmediumitc', 'felixtitling', 'forte', 'franklingothicbook',
         'franklingothicbookkursiv', 'franklingothicdemi', 'franklingothicdemicond', 'franklingothicdemikursiv',
         'franklingothicheavy', 'franklingothicheavykursiv', 'franklingothicmediumcond', 'freestylescript',
         'frenchscript', 'footlight', 'garamond', 'garamondfett', 'garamondkursiv', 'gigi', 'gillsansfettkursiv',
         'gillsansfett', 'gillsanscondensed', 'gillsanskursiv', 'gillsansultracondensed', 'gillsansultra', 'gillsans',
         'gloucesterextracondensed', 'gillsansextcondensed', 'centurygothic', 'centurygothicfett',
         'centurygothicfettkursiv', 'centurygothickursiv', 'goudyoldstyle', 'goudyoldstylefett', 'goudyoldstylekursiv',
         'goudystout', 'harlowsolid', 'harrington', 'haettenschweiler', 'hightowertext', 'hightowertextkursiv',
         'imprintshadow', 'informalroman', 'blackadderitc', 'edwardianscriptitc', 'kristenitc', 'jokerman', 'juiceitc',
         'kunstlerscript', 'widelatin', 'lucidabright', 'lucidacalligraphy', 'leelawadeefett', 'lucidafax',
         'lucidafaxhalbfett', 'lucidafaxhalbfettkursiv', 'lucidafaxkursiv', 'lucidahandwritingkursiv',
         'lucidasanshalbfett', 'lucidasanshalbfettkursiv', 'lucidasanskursiv', 'lucidasanstypewriter',
         'lucidasanstypewriterfett', 'lucidasanstypewriterfettschräg', 'lucidasanstypewriterschräg', 'magnetofett',
         'maiandragd', 'maturascriptcapitals', 'mistral', 'modernno20', 'microsoftuighurfett', 'monotypecorsiva',
         'niagaraengraved', 'niagarasolid', 'ocraextended', 'oldenglishtext', 'onyx', 'msoutlook', 'palacescript',
         'papyrus', 'parchment', 'perpetuafettkursiv', 'perpetuafett', 'perpetuakursiv', 'perpetuatitlingfett',
         'perpetuatitlingmager', 'perpetua', 'playbill', 'poorrichard', 'pristina', 'rage', 'ravie',
         'msreferencesansserif', 'msreferencespecialty', 'rockwellcondensedfett', 'rockwellcondensed', 'rockwell',
         'rockwellfett', 'rockwellfettkursiv', 'rockwellextra', 'rockwellkursiv', 'centuryschoolbookfett',
         'centuryschoolbookfettkursiv', 'centuryschoolbookkursiv', 'script', 'showcardgothic', 'snapitc', 'stencil',
         'twcenfettkursiv', 'twcenfett', 'twcencondensedfett', 'twcencondensedextra', 'twcencondensed', 'twcenkursiv',
         'twcen', 'tempussansitc', 'vinerhanditc', 'vivaldikursiv', 'vladimirscript', 'wingdings2', 'wingdings3',
         'extra', 'arialms', 'lucidahandwriting', 'brushscript', 'lucidafaxregular', 'magneto', 'perpetuatitling',
         'berlinsansfbdemi', 'lucidasanstypewriteroblique', 'lucidasansroman', 'zwadobef', 'eurosign',
         'lucidabrightregular', 'lucidasansregular', 'lucidasanstypewriterregular', 'hpsimplified', 'hpsimplifiedbdit',
         'hpsimplifiedit', 'hpsimplifiedlt', 'hpsimplifiedltit', 'hpsimplifiedrg', 'hpsimplifiedjpanlight',
         'hpsimplifiedjpanregular', 'hpsimplifiedhanslight', 'hpsimplifiedhansregular']'''

    def draw(self, world):
        if not self.old_window_width == world.windowWidth or not self.old_window_height == world.windowHeight:
            self.scale_to_window_size(world.windowWidth, world.windowHeight)
            self.old_window_width = world.windowWidth
            self.old_window_height = world.windowHeight
            print("unequal image sizes!!!!!!!!!!!")
        self.draw_health_bar(world)
        self.draw_stamina_bar(world)
        self.draw_mana_bar(world)

    def draw_health_bar(self, world):
        cropped_region = (0, 0, int(self.bar_width*(self.player.HP / self.player.maxHP* 3/4 + 1/4)), self.bar_height)
        world.window.blit(self.health_bar_image_inner_to_draw, self.health_bar_position, cropped_region)
        world.window.blit(self.health_bar_image_to_draw, self.health_bar_position)


        number_img = self.font.render(str(int(self.player.HP)), True, (0, 0, 0))
        world.window.blit(number_img, (self.health_bar_position[0] + self.bar_width, self.health_bar_position[1]))


    def draw_stamina_bar(self, world):
        world.window.blit(self.stamina_bar_image_to_draw, self.stamina_bar_position)

    def draw_mana_bar(self, world):
        world.window.blit(self.mana_bar_image_to_draw, self.mana_bar_position)


